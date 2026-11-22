"""Offline mechanical gates. Not a trusted signer or mathematical proof checker."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import os

try:
    from jsonschema import Draft202012Validator
except ImportError:
    raise SystemExit("DEPENDENCY_MISSING: install the declared jsonschema dependency; never assume PASS")

SCHEMAS = Path(__file__).resolve().parent.parent / 'schemas'
GATES = ['G1','G2','G2.5','G3','G4A','G4B','G5','G6']
LIMITS = ['Mechanical checks do not prove mathematical correctness or actual execution.',
          'A quoted local source supports traceability, not authenticated human identity.',
          'A writer with filesystem access can bypass or modify these tools; no security sandbox is claimed.']

class Invalid(ValueError): pass

def need(ok, message):
    if not ok: raise Invalid(message)

def now(): return datetime.now(timezone.utc).isoformat()
def digest(data): return hashlib.sha256(data).hexdigest()
def canonical(data): return json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def pairs(items):
    out={}
    for k,v in items:
        need(k not in out,'DUPLICATE_JSON_KEY: '+k)
        out[k]=v
    return out

def parse_bytes(data):
    def invalid_constant(x): raise Invalid('NONFINITE_JSON: '+x)
    return json.loads(data.decode('utf-8-sig'),object_pairs_hook=pairs,parse_constant=invalid_constant)

def pointer(data, ptr):
    need(ptr=='' or ptr.startswith('/'),'JSON_POINTER_REQUIRED')
    if ptr=='': return data
    for part in ptr[1:].split('/'):
        need(not re.search(r'~(?![01])',part),'INVALID_POINTER_ESCAPE')
        key=part.replace('~1','/').replace('~0','~')
        if isinstance(data,list):
            need(bool(re.fullmatch(r'0|[1-9][0-9]*',key)),'INVALID_ARRAY_POINTER')
            data=data[int(key)]
        else:
            need(isinstance(data,dict) and key in data,'MISSING_POINTER: '+ptr)
            data=data[key]
    return data

class Workspace:
    def __init__(self, root):
        self.root=Path(root).resolve(); self.checked={}; self.active=set();self.cache={}
        need(self.root.is_dir(),'WORKSPACE_MISSING')
    def path(self, rel):
        need(isinstance(rel,str) and rel and '\\' not in rel and ':' not in rel,'RELATIVE_POSIX_PATH_REQUIRED: '+str(rel))
        p=PurePosixPath(rel)
        need(not p.is_absolute() and '..' not in p.parts,'PATH_ESCAPE: '+rel)
        full=(self.root/rel).resolve()
        need(full.is_relative_to(self.root),'PATH_ESCAPE: '+rel)
        return full
    def raw(self, rel):
        p=self.path(rel);need(p.is_file(),'MISSING_FILE: '+rel)
        data=p.read_bytes();self.checked[rel]=digest(data);return data
    def ref(self, rel): return {'path':rel,'sha256':digest(self.raw(rel))}
    def validate_schema(self, data, kind):
        path=SCHEMAS/(kind+'.schema.json');need(path.is_file(),'UNKNOWN_SCHEMA: '+kind)
        schema=json.loads(path.read_text(encoding='utf-8'))
        errors=sorted(Draft202012Validator(schema).iter_errors(data),key=lambda e:str(list(e.path)))
        need(not errors,'SCHEMA: '+kind+' '+('; '.join(str(list(e.path))+': '+e.message for e in errors[:3])))
    def reference(self, reference):
        rel=reference['path'];data=self.raw(rel)
        need(digest(data)==reference['sha256'],'STALE_HASH: '+rel)
        # Recursively check registered machine artifacts, never infer a schema for raw metrics.
        if rel.endswith('.json'):
            j=parse_bytes(data)
            if isinstance(j,dict) and 'artifact_type' in j: self.artifact(rel,j['artifact_type'])
        return data
    def artifact(self, rel, kind):
        need(rel not in self.active,'CYCLIC_ARTIFACT_DEPENDENCY: '+rel)
        data=parse_bytes(self.raw(rel)); self.validate_schema(data,kind)
        self.active.add(rel)
        try:
            def walk(x):
                if isinstance(x,dict):
                    if 'path' in x and 'sha256' in x: self.reference(x)
                    for v in x.values(): walk(v)
                elif isinstance(x,list):
                    for v in x: walk(v)
            walk(data)
        finally: self.active.remove(rel)
        return data
    def checks(self, checks, required=(), allow_na=True):
        need(set(required)<=set(checks),'MISSING_NAMED_CHECKS: '+','.join(sorted(set(required)-set(checks))))
        for name,c in checks.items():
            need(c['status']=='PASS' or (allow_na and c['status']=='NOT_APPLICABLE'),'CHECK_NOT_PASS: '+name)
            need(bool(c['reason'].strip()),'EMPTY_REASON: '+name)
            if c['status']=='PASS':need(bool(c['evidence']),'NO_CHECK_EVIDENCE: '+name)
            for ref in c['evidence']:self.reference(ref)
    def binds(self, artifact, paths):
        refs={v['path']:v['sha256'] for v in artifact.get('inputs',[])}
        for path in paths:
            need(path in refs,'MISSING_INPUT_BINDING: '+path)
            need(refs[path]==digest(self.raw(path)),'STALE_BINDING: '+path)
    def decisions(self, q):
        rel=f'methods/{q}/{q.lower()}_decisions.jsonl'
        rows=[];ids=set();superseded=set()
        for line in self.raw(rel).splitlines():
            if not line.strip():continue
            d=parse_bytes(line);self.validate_schema(d,'decision')
            need(d['question_id']==q,'DECISION_QUESTION_MISMATCH')
            need(d['decision_id'] not in ids,'DUPLICATE_DECISION_ID')
            if d['decision_type']=='decision_stale':need(bool(d.get('supersedes')),'STALE_RECORD_MUST_NAME_SUPERSEDED_DECISION')
            if d.get('supersedes'):
                need(d['supersedes'] in ids,'INVALID_SUPERSESSION')
                superseded.add(d['supersedes'])
            ids.add(d['decision_id']);rows.append(d)
        # Old evidence may be stale. Validate only the live records when used.
        return [d for d in rows if d['decision_id'] not in superseded and d['status']=='DECIDED']
    def decision(self,q,kind,id=None):
        rows=[d for d in self.decisions(q) if d['decision_type']==kind and (id is None or d['decision_id']==id)]
        need(bool(rows),'MISSING_DECISION: '+q+' '+kind)
        d=rows[-1];src=d['source']
        need(src['provenance']!='legacy_unverified','UNVERIFIED_DECISION_SOURCE')
        raw=self.reference(src).decode('utf-8-sig')
        need(src['quote'] in raw,'DECISION_QUOTE_NOT_FOUND')
        need(d['rationale'].strip() and d['choice'] not in ('',[],{}),'EMPTY_DECISION')
        for ref in d['evidence_refs']:self.reference(ref)
        need(bool(d['evidence_refs']),'DECISION_WITHOUT_EVIDENCE')
        return d
    def decision_binds(self,d,paths):
        self.binds({'inputs':d['evidence_refs']},paths)
    def questions(self):
        p=self.artifact('planning/parse/problem_parse.json','problem-parse')
        ids=[q['id'] for q in p['subquestions']]
        need(len(set(ids))==len(ids),'DUPLICATE_QUESTION')
        return ids
    def run(self,q):
        m=self.artifact(f'planning/manifests/{q}.json','manifest')
        need(m['question_id']==q and m['latest_run'] is not None,'LATEST_RUN_MISSING')
        ref=m['latest_run'];rel=ref['path']
        need(bool(re.fullmatch(r'results/'+re.escape(q)+r'/experiments/[^/]+/run_summary.json',rel)),'NONCANONICAL_RUN_PATH')
        self.reference(ref);run=self.artifact(rel,'run-summary')
        need(run['question_id']==q,'RUN_QUESTION_MISMATCH')
        return rel,run
    def fingerprint(self,q):
        rel,run=self.run(q)
        return digest(canonical({'selected_output':run['selected_output'],'source_run':self.ref(rel)}))
    def report(self,q,kind,path,required_inputs):
        a=self.artifact(path,'report-binding')
        need(a['question_id']==q and a['report_kind']==kind,'REPORT_BINDING_MISMATCH')
        need(a['report']['path']!=path,'SELF_REPORT_BINDING')
        self.reference(a['report']);self.binds(a,required_inputs)
        return a
    def selected_ready(self,q):
        rel,run=self.run(q)
        rp=f'robustness/{q}/{q.lower()}_robustness_summary.json'
        rob=self.artifact(rp,'robustness')
        need(rob['verdict']=='PASS','ROBUSTNESS_NOT_PASS: completion requires resolved scope and checks')
        self.checks(rob['checks'])
        obligations=run['output_obligations'];ids=[o['id'] for o in obligations]
        need(len(ids)==len(set(ids)) and all(o['satisfied'] for o in obligations),'OUTPUT_OBLIGATIONS_UNRESOLVED')
        for o in obligations:
            need(bool(o['evidence']),'OBLIGATION_EVIDENCE_MISSING')
            for ref in o['evidence']:self.reference(ref)
        return rel,run
    def gate(self,q,target):
        need(target in GATES,'UNKNOWN_GATE: '+target)
        need(bool(re.fullmatch(r'Q[0-9]+(?:[._-][A-Za-z0-9]+)*',q)),'INVALID_QUESTION_ID')
        n=GATES.index(target)
        config=self.artifact('planning/session_config.json','session')
        parse=self.artifact('planning/parse/problem_parse.json','problem-parse')
        need(not parse['missing_material'] and not parse['human_decisions_needed'],'FRAMING_UNRESOLVED')
        for ref in parse['problem_source']:self.reference(ref)
        qs=[x for x in parse['subquestions'] if x['id']==q];need(len(qs)==1,'QUESTION_NOT_UNIQUE')
        for dep in qs[0]['cross_question_dependencies']:
            need(dep['upstream_question']!=q,'SELF_QUESTION_DEPENDENCY')
            self.reference(dep['artifact'])
            upstream=parse_bytes(self.raw(dep['artifact']['path']))
            status=upstream.get('status',upstream.get('verdict'))
            need(status==dep['required_status'],'UPSTREAM_STATUS_MISMATCH')
        cl=self.artifact('planning/classification/problem_classification.json','problem-classification')
        self.binds(cl,['planning/parse/problem_parse.json'])
        need(sorted(x['id'] for x in cl['subquestions'])==sorted(x['id'] for x in parse['subquestions']),'CLASSIFICATION_COVERAGE_MISMATCH')
        dp=self.artifact('planning/data/data_profile.json','data-profile')
        need(dp['per_question_readiness'].get(q) in ('ready','ready_with_warnings','not_applicable'),'DATA_NOT_READY')
        for ref in dp['raw_files']+dp['cleaned_files']:self.reference(ref)
        framing=self.decision(q,'framing');self.decision_binds(framing,['planning/parse/problem_parse.json'])
        if n==0:return
        cardp=f'methods/{q}/{q.lower()}_method_card.json'
        card=self.artifact(cardp,'method-card');need(card['question_id']==q,'METHOD_QUESTION_MISMATCH')
        methods=card['methods'];ids=[m['method_id'] for m in methods]
        need(len(set(ids))==len(ids),'DUPLICATE_METHOD')
        main=[m for m in methods if m['role']=='main_candidate'];base=[m for m in methods if m['role']=='usable_baseline']
        need(len(main)==len(base)==1,'MAIN_BASELINE_CARDINALITY')
        need(sum(m['role']=='conditional_fallback' for m in methods)<=1,'TOO_MANY_FALLBACKS')
        for m in methods:
            if m['role']=='conditional_fallback':need(bool(m.get('fallback_trigger','').strip()),'FALLBACK_TRIGGER_MISSING')
        need(card['baseline_validity']['completes_task'] and card['baseline_validity']['comparable'],'INVALID_BASELINE_DECLARATION')
        probep=f'methods/{q}/probes/risk_probe_summary.json'
        probe=self.artifact(probep,'risk-probe');self.binds(probe,[cardp])
        need(probe['question_id']==q,'PROBE_QUESTION_MISMATCH')
        for m in main+base:
            found=[p for p in probe['methods'] if p['method_id']==m['method_id']]
            need(len(found)==1 and found[0]['verdict'] in ('PASS','CONDITIONAL'),'METHOD_PROBE_FAILED')
            self.checks(found[0]['checks'])
        if n==1:return
        choice=self.decision(q,'method_choice');self.decision_binds(choice,[cardp,probep])
        required={m['method_id'] for m in main+base}
        need(set(choice.get('selected_methods',[]))==required,'METHOD_CHOICE_MISMATCH')
        if n==2:return
        runp,run=self.run(q)
        need(run['approved_decision_id']==choice['decision_id'],'RUN_DECISION_MISMATCH')
        self.binds(run,[cardp,probep,'planning/parse/problem_parse.json','planning/data/data_profile.json'])
        runids=[m['method_id'] for m in run['methods']]
        need(len(runids)==len(set(runids)) and required<=set(runids),'MAIN_BASELINE_RUN_MISSING')
        mapping={m['method_id']:m for m in methods}
        for m in run['methods']:
            need(m['method_id'] in mapping,'UNAPPROVED_RUN_METHOD')
            expected={'main_candidate':'main','usable_baseline':'usable_baseline','conditional_fallback':'conditional_fallback'}.get(mapping[m['method_id']]['role'])
            need(m['role']==expected,'RUN_ROLE_MISMATCH')
            if expected=='conditional_fallback':
                activation=self.decision(q,'fallback_activation')
                need(m['method_id'] in activation.get('selected_methods',[]),'FALLBACK_ACTIVATION_MISMATCH')
                self.decision_binds(activation,[cardp,probep])
            need(m['status']=='success','RUN_NOT_SUCCESS: '+m['method_id'])
            need(not m['constraint_violations'],'HARD_CONSTRAINT_VIOLATION')
            need(m['script']['path'].startswith(f"code/{q}/{m['language']}/"),'NONCANONICAL_CODE_PATH')
            self.reference(m['script'])
            for ref in m['outputs']:
                need(ref['path'].startswith(f'results/{q}/'),'NONCANONICAL_OUTPUT_PATH')
                self.reference(ref)
        need(run['selected_output']['method_id'] in runids,'SELECTED_METHOD_MISSING')
        for lang in {m['language'] for m in run['methods']}:
            reviewp=f'code/{q}/reviews/{q.lower()}_{lang}_review.json'
            review=self.artifact(reviewp,'review')
            need(review['question_id']==q and review['language']==lang,'REVIEW_IDENTITY_MISMATCH')
            self.binds(review,[runp]+[m['script']['path'] for m in run['methods'] if m['language']==lang])
            need(all(ref['path']!=reviewp for c in review['checks'].values() for ref in c['evidence']),'SELF_REVIEW_EVIDENCE')
            required_checks=['syntax','input_contract','method_alignment','reproducibility','output_contract']
            self.checks(review['checks'],required_checks)
            need(all(review['checks'][k]['status']=='PASS' for k in required_checks),'CORE_REVIEW_NOT_RUN')
        population=run.get('contract_evidence',{}).get('input_population_contract',{})
        if population.get('status')=='APPLICABLE':
            for key in ['audited','parsed','excluded','eligible']:
                need(type(population.get(key)) is int and population[key]>=0,'INVALID_POPULATION_COUNT')
            need(population['audited']==population['parsed'] and population['parsed']-population['excluded']==population['eligible'],'POPULATION_LOSS')
            used=population.get('used_by_method',{})
            need(all(used.get(i)==population['eligible'] for i in required),'COMPARISON_POPULATION_MISMATCH')
        if n==3:return
        robp=f'robustness/{q}/{q.lower()}_robustness_summary.json'
        rob=self.artifact(robp,'robustness');self.binds(rob,[runp])
        need(rob['question_id']==q and rob['selected_fingerprint']==self.fingerprint(q),'ROBUSTNESS_SELECTION_MISMATCH')
        # Results may be judged as failed; freezing for completion is a separate gate.
        for c in rob['checks'].values():
            need(bool(c['reason'].strip()),'ROBUSTNESS_REASON_MISSING')
            for ref in c['evidence']:self.reference(ref)
        for kind in ['result_verdict','stability_verdict','claim_scope']:
            d=self.decision(q,kind);self.decision_binds(d,[runp,robp])
        if n==4:return
        need(config['rigor_profile']=='submission','SUBMISSION_PROFILE_REQUIRED')
        self.selected_ready(q)
        self.verify_freeze(q)
        for kind,suffix in [('method_explanation','method_explanation'),('final_analysis','final_analysis'),('robustness_report','robustness_report'),('writer_package','writer_package')]:
            self.report(q,kind,f'results/{q}/reports/{suffix}.json',[runp,robp])
        if n==5:return
        freezep=f'results/{q}/reports/frozen_numbers.json'
        self.report(q,'paper_section',f'paper/sections/{q.lower()}.json',[freezep])
        fp=self.artifact(f'methods/{q}/{q.lower()}_figure_table_plan.json','figure-plan')
        need(fp['question_id']==q,'FIGURE_QUESTION_MISMATCH')
        if not fp['figures']:need(bool(fp['no_visual_reason'].strip()),'NO_VISUAL_REASON_REQUIRED')
        fids=[f['id'] for f in fp['figures']];need(len(fids)==len(set(fids)),'DUPLICATE_FIGURE')
        for f in fp['figures']:
            need(f['question_id']==q,'FIGURE_QUESTION_MISMATCH')
            for ref in f['source_artifacts']:self.reference(ref)
            if f['type'] in (2,3,4) and f['status']!='omitted':
                need(f['status']=='rendered' and f['output'] is not None and f['render_check'] is not None,'FIGURE_NOT_RENDERED')
                self.reference(f['output']);self.checks({'render':f['render_check']},allow_na=False)
                if f['type']==3:
                    self.decision(q,'claim_scope',f.get('decision_id'))
                    self.binds({'inputs':f['source_artifacts']},[freezep])
            if f['type']==1:need(not f.get('target_section'),'DIAGNOSTIC_IN_PAPER')
        if n==6:return
        self.final_audits()
    def verify_freeze(self,q,allow_evidence=False):
        rel=f'results/{q}/reports/frozen_numbers.json'
        freeze=self.artifact(rel,'frozen-numbers')
        need(freeze['question_id']==q,'FREEZE_QUESTION_MISMATCH')
        need(allow_evidence or freeze['mode']=='complete','EVIDENCE_FREEZE_NOT_COMPLETION')
        need(freeze['selected_fingerprint']==self.fingerprint(q),'FREEZE_SELECTION_MISMATCH')
        planp=f'results/{q}/reports/freeze_plan.json';plan=self.artifact(planp,'freeze-plan')
        need(plan['question_id']==q,'FREEZE_PLAN_QUESTION_MISMATCH')
        d=self.decision(q,'package_signoff',freeze['decision_id']);runp,_=self.run(q)
        self.decision_binds(d,[planp,runp]);self.binds(freeze,[planp,runp,f'methods/{q}/{q.lower()}_decisions.jsonl'])
        planned={c['claim_id']:c for c in plan['claims']}
        need(len(planned)==len(plan['claims']),'DUPLICATE_CLAIM_ID')
        need(len(freeze['claims'])==len(planned) and {c['claim_id'] for c in freeze['claims']}==set(planned),'FREEZE_CLAIM_MISMATCH')
        _, current_run=self.run(q)
        selected_paths={o['path'] for m in current_run['methods'] if m['method_id']==current_run['selected_output']['method_id'] for o in m['outputs']}
        for c in freeze['claims']:
            need(c['source_file'] in selected_paths,'CLAIM_NOT_SELECTED_OUTPUT')
            pc=planned[c['claim_id']]
            need(all(c[k]==pc[k] for k in ['source_file','source_pointer','unit']),'FREEZE_SOURCE_CHANGED')
            data=self.reference({'path':c['source_file'],'sha256':c['source_sha256']})
            value=pointer(parse_bytes(data),c['source_pointer'])
            need(type(value) in (int,float) and math.isfinite(value) and value==c['value'],'FROZEN_VALUE_MISMATCH')
        return freeze
    def audit(self,kind,questions):
        rel=f'paper/audits/{kind}.json';a=self.artifact(rel,'audit')
        need(a['audit_kind']==kind and set(a['scope'])==set(questions),'AUDIT_SCOPE_MISMATCH')
        banned={rel}
        if kind=='consistency':banned|={'paper/audits/completeness.json','paper/audits/qa.json'}
        if kind=='completeness':banned.add('paper/audits/qa.json')
        evidence=a['inputs']+[ref for c in a['checks'].values() for ref in c['evidence']]
        need(not any(ref['path'] in banned for ref in evidence),'AUDIT_SELF_OR_DOWNSTREAM_DEPENDENCY')
        required={'consistency':['numbers','symbols','methods','claims','references','freshness'],
                  'completeness':['required_artifacts','evidence_fields','freshness'],
                  'qa':['workflow_integrity','evidence_integrity','method_quality','paper_quality','presentation']}[kind]
        self.checks(a['checks'],required,allow_na=False)
        need(not any(f['severity']=='BLOCKER' for f in a['findings']),'AUDIT_BLOCKER')
        bind=[]
        for q in questions:
            bind.extend([f'results/{q}/reports/frozen_numbers.json',f'paper/sections/{q.lower()}.json',f'methods/{q}/{q.lower()}_figure_table_plan.json'])
        bind.extend(['planning/symbols.json','planning/assumptions.json','paper/references.json'])
        if kind in ('completeness','qa'):bind.append('paper/audits/consistency.json')
        if kind=='qa':bind.append('paper/audits/completeness.json')
        self.binds(a,bind)
    def final_audits(self,stage='qa'):
        qs=self.questions()
        for q in qs:self.gate(q,'G5')
        for kind,path in [('symbols','planning/symbols.json'),('assumptions','planning/assumptions.json'),('references','paper/references.json')]:
            self.report(None,kind,path,[])
        for kind in ['consistency','completeness','qa']:
            self.audit(kind,qs)
            if stage==kind:break
    def result(self,q,gate,errors):
        profile='unknown'
        try:profile=parse_bytes(self.raw('planning/session_config.json')).get('rigor_profile','unknown')
        except (ValueError,OSError):pass
        return dict(schema_version=2,artifact_type='gate-result',question_id=q,requested_gate=gate,profile=profile,
                    mechanical_status='FAIL' if errors else 'PASS',errors=errors,
                    checked_files=[{'path':p,'sha256':s} for p,s in sorted(self.checked.items())],generated_at=now(),generator='gate_engine.py',limits=LIMITS)


def atomic_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.gate-',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(canonical(data)+b'\n')
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def freeze_results(w,q,mode,replace_reason=None):
    w.gate(q,'G4A')
    config=w.artifact('planning/session_config.json','session')
    if mode=='complete':
        need(config['rigor_profile']=='submission','SUBMISSION_PROFILE_REQUIRED');w.selected_ready(q)
    runp,current_run=w.run(q);planp=f'results/{q}/reports/freeze_plan.json'
    plan=w.artifact(planp,'freeze-plan');need(plan['question_id']==q,'FREEZE_PLAN_QUESTION_MISMATCH')
    d=w.decision(q,'package_signoff');w.decision_binds(d,[planp,runp])
    claims=[];ids=set()
    selected_paths={o['path'] for m in current_run['methods'] if m['method_id']==current_run['selected_output']['method_id'] for o in m['outputs']}
    for c in plan['claims']:
        need(c['source_file'] in selected_paths,'CLAIM_NOT_SELECTED_OUTPUT')
        need(c['claim_id'] not in ids,'DUPLICATE_CLAIM_ID');ids.add(c['claim_id'])
        need(c['source_file'].startswith(f'results/{q}/experiments/'),'NONCANONICAL_CLAIM_SOURCE')
        data=w.raw(c['source_file']);value=pointer(parse_bytes(data),c['source_pointer'])
        need(type(value) in (int,float) and math.isfinite(value),'CLAIM_NOT_FINITE_NUMBER')
        claims.append(c|{'source_sha256':digest(data),'value':value})
    frozen=dict(schema_version=2,artifact_type='frozen-numbers',question_id=q,mode=mode,created_at=now(),generator='freeze_results.py',selected_fingerprint=w.fingerprint(q),decision_id=d['decision_id'],claims=claims,
                inputs=[w.ref(p) for p in [planp,runp,f'methods/{q}/{q.lower()}_decisions.jsonl']])
    w.validate_schema(frozen,'frozen-numbers')
    # Refuse writes when anything checked changed during this command.
    for rel,sha in list(w.checked.items()):need(digest(w.path(rel).read_bytes())==sha,'INPUT_CHANGED_DURING_FREEZE: '+rel)
    dest=w.path(f'results/{q}/reports/frozen_numbers.json')
    if dest.exists():
        need(bool(replace_reason and replace_reason.strip()),'EXISTING_FREEZE: --replace-reason required')
        previous=dest.read_bytes();oldhash=digest(previous)
        history=dest.parent/'freeze_history'/f'{oldhash}.json'
        history.parent.mkdir(parents=True,exist_ok=True)
        if not history.exists():history.write_bytes(previous)
        log=dest.parent/'freeze_change_log.md'
        with log.open('a',encoding='utf-8') as f:f.write(f"\n- {now()} | prior={oldhash} | {replace_reason}\n")
    atomic_json(dest,frozen)
    return frozen


def main(command):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--workspace',required=True);ap.add_argument('--question');ap.add_argument('--output')
    if command in ('validate_gate','validate_workspace'):ap.add_argument('--gate',choices=GATES,default='G3')
    if command=='validate_workspace':ap.add_argument('--audit-stage',choices=['consistency','completeness','qa'])
    if command=='check_staleness':ap.add_argument('--artifact',required=True)
    if command=='freeze_results':
        ap.add_argument('--mode',choices=['complete','evidence_only'],default='complete');ap.add_argument('--replace-reason')
    args=ap.parse_args();w=Workspace(args.workspace);errors=[]
    gate=getattr(args,'gate',command)
    try:
        if command=='validate_gate':need(bool(args.question),'QUESTION_REQUIRED');w.gate(args.question,args.gate)
        elif command=='validate_workspace':
            if args.audit_stage:w.final_audits(args.audit_stage);gate='audit:'+args.audit_stage
            else:
                for q in w.questions():w.gate(q,args.gate)
        elif command=='check_staleness':
            a=parse_bytes(w.raw(args.artifact));w.artifact(args.artifact,a['artifact_type'])
            # Recheck referenced outputs and source bindings, not only input timestamps.
            def walk(x):
                if isinstance(x,dict):
                    if 'path' in x and 'sha256' in x:w.reference(x)
                    for v in x.values():walk(v)
                elif isinstance(x,list):
                    for v in x:walk(v)
            walk(a)
            if a['artifact_type']=='frozen-numbers':w.verify_freeze(a['question_id'],allow_evidence=True)
        elif command=='freeze_results':need(bool(args.question),'QUESTION_REQUIRED');freeze_results(w,args.question,args.mode,args.replace_reason)
        else:raise Invalid('UNKNOWN_COMMAND')
    except (Invalid,OSError,KeyError,IndexError,TypeError,ValueError,RecursionError) as e:errors.append(str(e))
    result=w.result(args.question,gate,errors)
    if args.output:
        path=w.path(args.output)
        need(args.output.startswith('planning/gates/') and args.output.endswith('.json'),'GATE_OUTPUT_MUST_BE_UNDER_planning/gates')
        need(args.output not in w.checked,'CANNOT_OVERWRITE_CHECKED_INPUT')
        atomic_json(path,result)
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    return 1 if errors else 0
