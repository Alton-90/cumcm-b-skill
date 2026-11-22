"""Synthetic end-to-end gate fixtures and negative cases; not contest evidence."""
from pathlib import Path
import tempfile
import json
import sys
import hashlib
import copy
import subprocess
import os
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.codex/skills/workflow-orchestrator/scripts'))
from gate_engine import Workspace, Invalid, freeze_results, parse_bytes, SCHEMAS
from jsonschema import Draft202012Validator


def fixture(root,profile='submission'):
    w=Workspace(root)
    def text(path,value):
        p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value,encoding='utf-8')
    def put(path,kind,**fields):
        d=dict(schema_version=2,artifact_type=kind,**fields)
        w.validate_schema(d,kind);text(path,json.dumps(d,ensure_ascii=False));return path
    def refs(*paths):return [w.ref(p) for p in paths]
    def check(*paths):return dict(status='PASS',reason='Synthetic check fixture, not an actual contest review',evidence=refs(*paths))
    text('sources/problem.txt','Synthetic gate integration case')
    text('sources/user.txt','SYNTHETIC USER FIXTURE: approve this test configuration and its claims.')
    put('planning/session_config.json','session',interaction_mode='speed',rigor_profile=profile)
    parse=put('planning/parse/problem_parse.json','problem-parse',problem_source=refs('sources/problem.txt'),global_goal='Synthetic value comparison',subquestions=[dict(id='Q1',goal='Compare values',required_outputs=['score'],success_criteria=['registered score'],cross_question_dependencies=[])],missing_material=[],human_decisions_needed=[])
    put('planning/classification/problem_classification.json','problem-classification',inputs=refs(parse),subquestions=[dict(id='Q1',primary_type='optimization',evidence=['Q1 score'],required_validation=['feasibility'])])
    data=put('planning/data/data_profile.json','data-profile',raw_files=[],coverage={'rows':0},per_question_readiness={'Q1':'not_applicable'},cleaned_files=[],unresolved_risks=[])
    ledger='methods/Q1/q1_decisions.jsonl';records=[]
    def decision(kind,paths,**extra):
        d=dict(schema_version=2,artifact_type='decision',question_id='Q1',decision_id=kind,decision_type=kind,status='DECIDED',decided_by='human',source=w.ref('sources/user.txt')|dict(quote='approve this test configuration',locator='line 1',provenance='user_message_export'),choice='approve',rationale='Synthetic evidence-bound approval',evidence_refs=refs(*paths),decided_at='2026-09-10T00:00:00Z',**extra)
        w.validate_schema(d,'decision');records.append(d);text(ledger,'\n'.join(json.dumps(x) for x in records)+'\n')
    decision('framing',[parse])
    card=put('methods/Q1/q1_method_card.json','method-card',question_id='Q1',methods=[dict(method_id='M',role='main_candidate',name='Main',required_outputs=['score']),dict(method_id='B',role='usable_baseline',name='Baseline',required_outputs=['score'])],goal='Compare',baseline_validity=dict(completes_task=True,comparable=True,reason='Synthetic same output'))
    probe=put('methods/Q1/probes/risk_probe_summary.json','risk-probe',question_id='Q1',inputs=refs(card),methods=[dict(method_id=i,verdict='PASS',reason='Synthetic',checks={'executability':check('sources/problem.txt')}) for i in ['M','B']])
    decision('method_choice',[card,probe],selected_methods=['M','B'])
    runs=[]
    for i,role,score in [('M','main',2),('B','usable_baseline',1)]:
        script=f'code/Q1/python/{i}.py';metric=f'results/Q1/experiments/round1/metrics/{i}.json'
        text(script,f'print({score})\n');text(metric,json.dumps({'score':score}))
        runs.append(dict(method_id=i,role=role,status='success',language='python',script=w.ref(script),outputs=refs(metric),metrics_summary={'score':score},constraint_violations=[]))
    run=put('results/Q1/experiments/round1/run_summary.json','run-summary',question_id='Q1',round='round1',approved_decision_id='method_choice',methods=runs,comparison=dict(population_id='synthetic',metric_contract='score'),selected_output=dict(method_id='M',parameters={},composition=[],evaluator='synthetic score',resolution=1),output_obligations=[dict(id='score',satisfied=True,evidence=runs[0]['outputs'])],random_seed=0,environment={'fixture':True},inputs=refs(card,probe,parse,data))
    put('planning/manifests/Q1.json','manifest',question_id='Q1',latest_run=w.ref(run))
    put('code/Q1/reviews/q1_python_review.json','review',question_id='Q1',language='python',inputs=refs(run,*[x['script']['path'] for x in runs]),checks={k:check(run) for k in ['syntax','input_contract','method_alignment','reproducibility','output_contract']},findings=[],verdict='PASSED')
    rob=put('robustness/Q1/q1_robustness_summary.json','robustness',question_id='Q1',selected_fingerprint=w.fingerprint('Q1'),checks={'stability':check(run)},limitations=[],verdict='PASS',inputs=refs(run))
    for kind in ['result_verdict','stability_verdict','claim_scope']:decision(kind,[run,rob])
    plan=put('results/Q1/reports/freeze_plan.json','freeze-plan',question_id='Q1',claims=[dict(claim_id='score',source_file=runs[0]['outputs'][0]['path'],source_pointer='/score',unit='unitless')])
    decision('package_signoff',[plan,run])
    for kind in ['method_explanation','final_analysis','robustness_report','writer_package']:
        report=f'results/Q1/reports/{kind}.md';text(report,'Synthetic readable report')
        put(f'results/Q1/reports/{kind}.json','report-binding',question_id='Q1',report_kind=kind,report=w.ref(report),inputs=refs(run,rob))
    def complete(mode='complete'):
        freeze_results(Workspace(root),'Q1',mode)
        freeze='results/Q1/reports/frozen_numbers.json'
        text('paper/sections/q1.md','Synthetic score: 2')
        section=put('paper/sections/q1.json','report-binding',question_id='Q1',report_kind='paper_section',report=w.ref('paper/sections/q1.md'),inputs=refs(freeze))
        figure=put('methods/Q1/q1_figure_table_plan.json','figure-plan',question_id='Q1',figures=[],no_visual_reason='Single scalar needs no plot')
        globals=[]
        for kind,path in [('symbols','planning/symbols.json'),('assumptions','planning/assumptions.json'),('references','paper/references.json')]:
            report=path[:-5]+'.md';text(report,'Synthetic global report')
            put(path,'report-binding',question_id=None,report_kind=kind,report=w.ref(report),inputs=refs(parse));globals.append(path)
        prior=[]
        for kind,keys in [('consistency',['numbers','symbols','methods','claims','references','freshness']),('completeness',['required_artifacts','evidence_fields','freshness']),('qa',['workflow_integrity','evidence_integrity','method_quality','paper_quality','presentation'])]:
            put(f'paper/audits/{kind}.json','audit',audit_kind=kind,scope=['Q1'],checks={k:check(section) for k in keys},findings=[],inputs=refs(freeze,section,figure,*globals,*prior),verdict='PASSED')
            prior.append(f'paper/audits/{kind}.json')
    return complete


def main():
    results=[];base=Path(__file__).resolve().parents[1]/'tests';base.mkdir(exist_ok=True)
    def case(name,fn):
        with tempfile.TemporaryDirectory(prefix='gate-test-',dir=base) as tmp:
            root=Path(tmp).resolve()
            if not root.is_relative_to(base.resolve()):raise RuntimeError('test path escape')
            complete=fixture(root);fn(root,complete)
        results.append(dict(name=name,status='PASS'))
    def reject(root,gate='G3',contains=None):
        try: Workspace(root).gate('Q1',gate)
        except (Invalid,ValueError,KeyError) as e:
            if contains and contains not in str(e):raise AssertionError(str(e))
            return
        raise AssertionError('unexpected PASS')
    def mutate(root,path,fn):
        p=root/path;j=json.loads(p.read_text());fn(j);p.write_text(json.dumps(j))
    case('valid_G1_to_G4A',lambda r,c:[Workspace(r).gate('Q1',g) for g in ['G1','G2','G2.5','G3','G4A']])
    case('valid_freeze_and_G6',lambda r,c:(c(),Workspace(r).gate('Q1','G6')))
    def audit_order(r,c):
        c();(r/'paper/audits/qa.json').unlink();(r/'paper/audits/completeness.json').unlink()
        Workspace(r).final_audits('consistency')
    case('consistency_without_future_audits',audit_order)
    def completeness(r,c):
        c();(r/'paper/audits/qa.json').unlink();Workspace(r).final_audits('completeness')
    case('completeness_without_QA',completeness)
    case('missing_baseline_output',lambda r,c:((r/'results/Q1/experiments/round1/metrics/B.json').unlink(),reject(r)))
    case('self_asserted_PASS_ignored',lambda r,c:(mutate(r,'code/Q1/reviews/q1_python_review.json',lambda j:j['checks']['syntax'].update(status='FAIL')),reject(r,contains='CHECK_NOT_PASS')))
    case('missing_decision_source',lambda r,c:((r/'sources/user.txt').unlink(),reject(r)))
    case('stale_code_hash',lambda r,c:((r/'code/Q1/python/M.py').write_text('print(999)'),reject(r,contains='STALE_HASH')))
    case('stale_raw_source',lambda r,c:((r/'sources/problem.txt').write_text('changed'),reject(r,contains='STALE_HASH')))
    case('legacy_schema_rejected',lambda r,c:(mutate(r,'planning/parse/problem_parse.json',lambda j:j.update(schema_version=1)),reject(r,contains='SCHEMA')))
    case('unknown_field_rejected',lambda r,c:(mutate(r,'planning/session_config.json',lambda j:j.update(fake=True)),reject(r,contains='SCHEMA')))
    def lean(r,c):
        mutate(r,'planning/session_config.json',lambda j:j.update(rigor_profile='lean'))
        Workspace(r).gate('Q1','G4A');reject(r,'G4B','SUBMISSION_PROFILE_REQUIRED')
    case('lean_G4A_not_G4B',lean)
    case('evidence_only_not_completion',lambda r,c:(c('evidence_only'),reject(r,'G4B','EVIDENCE_FREEZE_NOT_COMPLETION')))
    case('tampered_frozen_value',lambda r,c:(c(),mutate(r,'results/Q1/reports/frozen_numbers.json',lambda j:j['claims'][0].update(value=999)),reject(r,'G4B','FROZEN_VALUE_MISMATCH')))
    case('stale_paper_text',lambda r,c:(c(),(r/'paper/sections/q1.md').write_text('score 999'),reject(r,'G5','STALE_HASH')))
    case('stale_robustness_selection',lambda r,c:(mutate(r,'robustness/Q1/q1_robustness_summary.json',lambda j:j.update(selected_fingerprint='0'*64)),reject(r,'G4A','ROBUSTNESS_SELECTION_MISMATCH')))
    def incomplete(r,c):
        mutate(r,'results/Q1/experiments/round1/run_summary.json',lambda j:j['output_obligations'][0].update(satisfied=False))
        reject(r,'G4B')
    case('changed_output_obligations_block',incomplete)
    def cycle(r,c):
        c();a=json.loads((r/'paper/audits/completeness.json').read_text())
        a['inputs'].append(Workspace(r).ref('paper/audits/qa.json'))
        (r/'paper/audits/completeness.json').write_text(json.dumps(a));reject(r,'G6')
    case('audit_downstream_cycle_blocked',cycle)
    def otherq(r,c):
        c();mutate(r,'planning/parse/problem_parse.json',lambda j:j['subquestions'].append(dict(id='Q2',goal='missing',required_outputs=['x'],success_criteria=['x'],cross_question_dependencies=[])))
        reject(r,'G6')
    case('changed_question_scope_blocked',otherq)
    def refreeze(r,c):
        c()
        try:freeze_results(Workspace(r),'Q1','complete')
        except Invalid as e:
            if 'EXISTING_FREEZE' not in str(e):raise
        else:raise AssertionError('overwrote snapshot')
        freeze_results(Workspace(r),'Q1','complete','Synthetic renewed freeze')
        if not list((r/'results/Q1/reports/freeze_history').glob('*.json')):raise AssertionError('missing archive')
    case('refreeze_requires_reason_preserves_history',refreeze)
    def escape(r,c):
        for path in ['../escape','C:/escape','/absolute']:
            try:Workspace(r).path(path)
            except Invalid:continue
            raise AssertionError('path accepted')
    case('path_escape_rejected',escape)
    try:parse_bytes(b'{"a":1,"a":2}')
    except Invalid:results.append(dict(name='duplicate_JSON_key',status='PASS'))
    else:raise AssertionError('duplicate accepted')
    for p in SCHEMAS.glob('*.json'):Draft202012Validator.check_schema(json.loads(p.read_text()))
    results.append(dict(name='all_schema_meta_validation',status='PASS'))
    def cli(r,c):
        run=subprocess.run([sys.executable,str(Path(__file__).with_name('validate_gate.py')),'--workspace',str(r),'--question','Q1','--gate','G3','--output','planning/gates/check.json'],capture_output=True,text=True)
        if run.returncode:raise AssertionError(run.stderr+run.stdout)
        j=json.loads(run.stdout);Workspace(r).validate_schema(j,'gate-result')
        (r/'sources/user.txt').unlink()
        run=subprocess.run([sys.executable,str(Path(__file__).with_name('validate_gate.py')),'--workspace',str(r),'--question','Q1','--gate','G3'],capture_output=True,text=True)
        if run.returncode!=1 or json.loads(run.stdout)['mechanical_status']!='FAIL':raise AssertionError('bad CLI fail')
    case('CLI_exit_codes_and_output_schema',cli)
    def stale_same_time(r,c):
        p=r/'code/Q1/python/M.py';old=p.stat();p.write_text('print(123)');os.utime(p,ns=(old.st_atime_ns,old.st_mtime_ns))
        reject(r,contains='STALE_HASH')
    case('hash_detects_change_with_same_timestamp',stale_same_time)
    def judged_failure(r,c):
        rob='robustness/Q1/q1_robustness_summary.json'
        mutate(r,rob,lambda j:(j.update(verdict='FAIL'),j['checks']['stability'].update(status='FAIL')))
        ledger=r/'methods/Q1/q1_decisions.jsonl';rows=[json.loads(x) for x in ledger.read_text().splitlines()]
        for d in rows:
            if d['decision_type'] in ['result_verdict','stability_verdict','claim_scope']:
                d['choice']='adjust';d['evidence_refs']=[Workspace(r).ref(x['path']) for x in d['evidence_refs']]
        ledger.write_text('\n'.join(json.dumps(x) for x in rows)+'\n')
        Workspace(r).gate('Q1','G4A');reject(r,'G4B','ROBUSTNESS_NOT_PASS')
    case('judged_failure_G4A_without_false_freeze',judged_failure)
    def all_cli(r,c):
        scripts=Path(__file__).parent
        cmds=[['freeze_results.py','--question','Q1'],['check_staleness.py','--artifact','results/Q1/reports/frozen_numbers.json'],['validate_workspace.py','--gate','G4A']]
        for command in cmds:
            proc=subprocess.run([sys.executable,str(scripts/command[0]),'--workspace',str(r),*command[1:]],capture_output=True,text=True)
            if proc.returncode or json.loads(proc.stdout)['mechanical_status']!='PASS':raise AssertionError(proc.stdout+proc.stderr)
    case('freeze_staleness_workspace_CLI',all_cli)
    def wrong_quote(r,c):
        ledger=r/'methods/Q1/q1_decisions.jsonl';rows=[json.loads(x) for x in ledger.read_text().splitlines()]
        rows[0]['source']['quote']='NOT IN SOURCE';ledger.write_text('\n'.join(json.dumps(x) for x in rows)+'\n')
        reject(r,contains='DECISION_QUOTE_NOT_FOUND')
    case('false_user_quote_rejected',wrong_quote)
    result=dict(scope='Synthetic integration/negative tests; not model or authentic-user verification',passed=len(results),results=results)
    out=Path(__file__).resolve().parents[1]/'docs/R6-runtime-tests.json';out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
