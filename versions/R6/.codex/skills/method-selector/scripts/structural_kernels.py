"""Conditional design kernels. Synthetic tests are not contest-performance evidence."""
import argparse
import math
import json
from pathlib import Path


def lookahead(state, depth, actions, transition, terminal_value):
    """Deterministic maximum cumulative reward plus terminal value.
    Returns (value, action tuple); requires depth>=0 and bounded branching.
    A nonterminal dead end has value -inf. Receding horizon executes only first action.
    """
    if not isinstance(depth,int) or depth < 0:
        raise ValueError('invalid depth')
    if depth == 0:
        return terminal_value(state), ()
    best = (-math.inf, ())
    for action in actions(state):
        next_state, reward = transition(state,action)
        value, tail = lookahead(next_state,depth-1,actions,transition,terminal_value)
        if reward+value > best[0]:
            best = reward+value, (action,)+tail
    return best


def known_circle_partner(c1, radius1, c2, radius2, known, tolerance=1e-9):
    """Reflect known common point across centers line. No noisy-data projection.
    Distinct centers required; tangent returns the same point.
    tolerance is a relative geometry tolerance with unit-scale floor.
    """
    vals=(*c1,*c2,*known,radius1,radius2,tolerance)
    if len(c1)!=2 or len(c2)!=2 or len(known)!=2 or any(not math.isfinite(x) for x in vals):
        raise ValueError('finite 2D geometry required')
    if min(radius1,radius2)<0 or tolerance<=0:
        raise ValueError('invalid radius/tolerance')
    dx,dy=c2[0]-c1[0],c2[1]-c1[1]
    scale=max(1,radius1,radius2)
    length=math.hypot(dx,dy)
    if length<=tolerance*scale:
        raise ValueError('coincident or ill-conditioned centers')
    if any(abs(math.dist(c,known)-rad)>tolerance*scale for c,rad in [(c1,radius1),(c2,radius2)]):
        raise ValueError('known point is not common to the circles')
    ux,uy=dx/length,dy/length
    projection=(known[0]-c1[0])*ux+(known[1]-c1[1])*uy
    foot=(c1[0]+projection*ux,c1[1]+projection*uy)
    return (2*foot[0]-known[0],2*foot[1]-known[1])


def renewal_value(reward, repeat_probability):
    """Single transient state, immediate net reward then repeat with probability q.
    Does not model quality-conditioning or multi-state assemblies by itself.
    """
    if not math.isfinite(reward) or not math.isfinite(repeat_probability) or not 0<=repeat_probability<1:
        raise ValueError('finite reward and absorbing probability required')
    return reward/(1-repeat_probability)


def disagreement_candidates(candidates, predictions, noise_scale, costs):
    """Heuristic max-min prediction spread / (noise scale * cost), descending.
    Not expected information gain; supplied predictions must share output units.
    """
    if len(predictions)<2 or not len(candidates)==len(noise_scale)==len(costs):
        raise ValueError('two models and aligned inputs required')
    if any(len(row)!=len(candidates) for row in predictions):
        raise ValueError('prediction shape mismatch')
    if any(not math.isfinite(v) for row in predictions for v in row):
        raise ValueError('nonfinite prediction')
    if any(not math.isfinite(v) or v<=0 for v in list(noise_scale)+list(costs)):
        raise ValueError('positive finite scales/costs required')
    result=[]
    for i,x in enumerate(candidates):
        spread=max(row[i] for row in predictions)-min(row[i] for row in predictions)
        result.append(dict(candidate=x,score=spread/noise_scale[i]/costs[i]))
    return sorted(result,key=lambda r:r['score'],reverse=True)


def self_test():
    checks=[]
    def check(name,ok):
        if not ok: raise AssertionError(name)
        checks.append(name)
    def rejects(name,fn):
        try: fn()
        except ValueError: checks.append(name); return
        raise AssertionError(name)
    # A costs an opportunity later; B has delayed gain. Same true two-step evaluator.
    graph={'s':{'A':('a',5),'B':('b',0)},'a':{'finish':('end',0)},'b':{'finish':('end',10)}}
    act=lambda s:list(graph.get(s,{}))
    tr=lambda s,a:graph[s][a]
    one=lookahead('s',1,act,tr,lambda s:0)
    two=lookahead('s',2,act,tr,lambda s:0)
    check('greedy_trap_first_action',one[1][0]=='A' and two[1][0]=='B')
    check('two_step_real_reward',sum([tr('s','A')[1],tr('a','finish')[1]])==5 and two[0]==10)
    # Counterexample: arbitrary terminal heuristic can prefer the worse true path.
    biased=lookahead('s',1,act,tr,lambda s:100 if s=='a' else 0)
    check('heuristic_has_no_optimality_guarantee',biased[1][0]=='A')
    check('dead_end_infeasible',lookahead('missing',1,act,tr,lambda s:0)[0]==-math.inf)
    c1,c2,known=(0.,0.),(2.,0.),(1.,2.)
    radius=math.sqrt(5)
    other=known_circle_partner(c1,radius,c2,radius,known)
    check('reflection_known_solution',math.dist(other,(1.,-2.))<1e-12)
    check('reflection_both_residuals',abs(math.dist(other,c1)-radius)<1e-12 and abs(math.dist(other,c2)-radius)<1e-12)
    def transform(p): return (-p[1]+3,p[0]-4)
    other2=known_circle_partner(transform(c1),radius,transform(c2),radius,transform(known))
    check('rotation_translation_invariance',math.dist(other2,transform(other))<1e-12)
    check('tangent_single_solution',known_circle_partner((0,0),1,(2,0),1,(1,0))==(1.,0.))
    rejects('coincident_rejected',lambda:known_circle_partner(c1,1,c1,1,(1,0)))
    rejects('invalid_common_point_rejected',lambda:known_circle_partner(c1,radius,c2,radius,(1,3)))
    value=renewal_value(-2,0.5)
    partial=sum(-2*0.5**k for k in range(30))
    check('renewal_known_value',value==-4)
    check('renewal_series_with_tail_bound',abs(partial-value)<=4*0.5**30+1e-12)
    check('renewal_no_repeat',renewal_value(3,0)==3)
    rejects('nonabsorbing_rejected',lambda:renewal_value(1,1))
    ranked=disagreement_candidates(['near','different'],[[10,0],[10,4]],[1,1],[1,1])
    check('experiment_discriminates_models',ranked[0]['candidate']=='different')
    ranked=disagreement_candidates(['noisy','informative'],[[0,0],[10,2]],[100,1],[1,1])
    check('raw_spread_not_enough',ranked[0]['candidate']=='informative')
    rejects('zero_noise_rejected',lambda:disagreement_candidates([1],[[1],[2]],[0],[1]))
    return dict(status='PASS',passed=len(checks),checks=checks,scope='synthetic mechanism and counterexample tests; no full contest or agent evaluation')


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    if not args.self_test: ap.error('import functions or specify --self-test')
    result=self_test();text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text+'\n',encoding='utf-8')
    print(text)
