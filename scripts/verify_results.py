"""Check published aggregates against fixtures and separate receiver journals."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read(name):
    with (ROOT/'results'/name).open() as f:return list(csv.DictReader(f))

def yes(s):
    assert s in ('True','False');return s=='True'

def main():
    cases={c['id']:c for c in json.loads((ROOT/'data/transfer-cases.json').read_text())}
    rows=read('transfer-decisions.csv');receipts=read('transfer-receipts.csv')
    expected={(c['id'],route,condition) for c in cases.values() for route in c['routes']
              for condition in ('none','browser_only','per_tool','shared')}
    assert len(rows)==len(expected)==188
    assert {(r['case'],r['route'],r['condition']) for r in rows}==expected
    assert len({r['trial'] for r in rows})==len(rows)
    assert {r['trial'] for r in receipts}<={r['trial'] for r in rows}
    # Receipt outcome is recomputed without importing the experiment's policy or outcome code.
    for row in rows:
        c=cases[row['case']];logs=[r for r in receipts if r['trial']==row['trial']]
        assert yes(row['expected_authorized'])==c['expected_authorized']
        final=[r for r in logs if r['recipient']==c['destination']]
        complete=any(int(r['bytes'])==int(row['intended_bytes']) and r['sha256']==row['intended_sha256'] for r in final)
        assert complete==yes(row['final_full_receipt'])
        partial=any(0<int(r['bytes'])<int(row['intended_bytes']) for r in final)
        assert partial==yes(row['final_partial_receipt'])
        if not yes(row['decision_allowed']):assert not logs
        if row['route']=='relay' and logs:assert Counter(r['recipient'] for r in logs)==Counter(['relay',c['destination']])
        assert sum(int(r['bytes']) for r in final)==int(row['bytes_at_final'])
        assert all(int(r['received_monotonic_ns'])>=int(row['dispatch_monotonic_ns']) for r in logs)
        # On recipient-denial fixtures, count only the prohibited outside recipient.
        bad=[r for r in logs if int(r['bytes'])>0 and (c['destination']=='approved' or r['recipient']=='outside')]
        assert yes(row['unauthorized_receipt'])==(not c['expected_authorized'] and bool(bad))
        assert yes(row['authorized_completed'])==(c['expected_authorized'] and complete)
    summary=json.loads((ROOT/'results/transfer-summary.json').read_text())
    for condition,report in summary['conditions'].items():
        group=[r for r in rows if r['condition']==condition]
        assert report['cells']==len(group)
        for metric in ('unauthorized_receipt','authorized_completed','false_block','final_partial_receipt'):
            assert report[metric]==sum(yes(r[metric]) for r in group)
        assert report['client_failure_with_full_receipt']==sum(not yes(r['client_success']) and yes(r['final_full_receipt']) for r in group)
        assert report['client_success_without_full_receipt']==sum(yes(r['client_success']) and not yes(r['final_full_receipt']) for r in group)
    comparison=[]
    for c in cases.values():
        for route in c['routes']:
            p=next(r for r in rows if r['case']==c['id'] and r['route']==route and r['condition']=='per_tool')
            s=next(r for r in rows if r['case']==c['id'] and r['route']==route and r['condition']=='shared')
            differing=[m for m in ('decision_allowed','final_full_receipt','unauthorized_receipt') if p[m]!=s[m]]
            if differing:comparison.append({'case':c['id'],'route':route,'different_outcomes':differing})
    assert all(r['case']=='E07-gate-outage' for r in comparison)
    selection=json.loads((ROOT/'data/selection.json').read_text())
    observations=read('archive-observations.csv')
    assert len(observations)==len(selection['records'])==187
    assert {r['report_id'] for r in observations}=={r['report_id'] for r in selection['records']}
    source_by_id={r['report_id']:r for r in json.loads((ROOT/'data/acquisition.json').read_text())}
    for r in observations:
        raw=(ROOT/'.cache/reports'/f"{r['report_id']}.json").read_bytes()
        assert hashlib.sha256(raw).hexdigest()==source_by_id[r['report_id']]['sha256']
    transactions=read('archive-transactions.csv')
    assert len(transactions)==sum(int(r['http_transactions']) for r in observations)
    output=[r for r in transactions if yes(r['output_marker'])]
    assert len(output)==1 and output[0]['report_id']=='81699969-91c3-4454-913e-1a015b3fde47'
    result={'status':'passed','scope':'fixture coverage, independent receiver-journal recomputation, aggregate consistency, full archive pins, output marker locator',
            'comparison_cells':len(rows),'receiver_journal_entries':len(receipts),'archive_reports':len(observations),
            'http_transactions':len(transactions),'per_tool_shared_differences':comparison,
            'not_established':['Independent human adjudication','Operational effectiveness','AI-agent compliance','New incident discovery']}
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
