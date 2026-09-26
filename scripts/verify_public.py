"""Verify shareable derived results and recompute experiment receipt outcomes.

Does not authenticate archive observations against third-party source JSON.
"""
import ast,csv,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
    with (ROOT/'results'/name).open() as f:return list(csv.DictReader(f))
def yes(x):
    assert x in ('True','False')
    return x=='True'
def main():
    decisions=rows('transfer-decisions.csv');receipts=rows('transfer-receipts.csv')
    cases={x['id']:x for x in json.loads((ROOT/'data/transfer-cases.json').read_text())}
    expected={(c['id'],route,condition) for c in cases.values() for route in c['routes'] for condition in ('none','browser_only','per_tool','shared')}
    assert len(decisions)==len(expected) and {(r['case'],r['route'],r['condition']) for r in decisions}==expected
    assert len({r['trial'] for r in decisions})==len(decisions)
    summary=json.loads((ROOT/'results/transfer-summary.json').read_text())
    # Read fixture bytes as literals; do not execute the producer or reuse its outcome logic.
    tree=ast.parse((ROOT/'scripts/transfer_experiment.py').read_text())
    fixtures=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='FIXTURES' for t in n.targets))
    assert {j['trial'] for j in receipts}<={r['trial'] for r in decisions}
    for r in decisions:
        c=cases[r['case']];journal=[j for j in receipts if j['trial']==r['trial']]
        final=[j for j in journal if j['recipient']==c['destination']]
        payload=fixtures[c['fixture']];size=len(payload);digest=hashlib.sha256(payload).hexdigest()
        assert int(r['intended_bytes'])==size and r['intended_sha256']==digest
        complete=any(int(j['bytes'])==size and j['sha256']==digest for j in final)
        partial=any(0<int(j['bytes'])<size for j in final)
        prohibited=[j for j in journal if int(j['bytes'])>0 and
                    (c['destination']=='approved' or j['recipient']=='outside')]
        assert complete==yes(r['final_full_receipt'])
        assert partial==yes(r['final_partial_receipt'])
        assert yes(r['unauthorized_receipt'])==(not c['expected_authorized'] and bool(prohibited))
        assert yes(r['false_block'])==(c['expected_authorized'] and not yes(r['decision_allowed']))
        assert yes(r['client_success'])==(r['client_status']=='200')
        assert int(r['bytes_at_final'])==sum(int(j['bytes']) for j in final)
        assert yes(r['expected_authorized'])==c['expected_authorized']
        if not yes(r['decision_allowed']):assert not journal
        assert yes(r['authorized_completed'])==(c['expected_authorized'] and complete)
    for condition,counts in summary['conditions'].items():
        group=[r for r in decisions if r['condition']==condition]
        for k in ('unauthorized_receipt','authorized_completed','false_block','final_partial_receipt'):
            assert counts[k]==sum(yes(r[k]) for r in group)
        assert counts['client_failure_with_full_receipt']==sum(not yes(r['client_success']) and yes(r['final_full_receipt']) for r in group)
        assert counts['client_success_without_full_receipt']==sum(yes(r['client_success']) and not yes(r['final_full_receipt']) for r in group)
    observations=rows('archive-observations.csv');transactions=rows('archive-transactions.csv')
    archive=json.loads((ROOT/'results/archive-summary.json').read_text())
    assert len(observations)==archive['retrieved']==187
    assert len(transactions)==archive['body_coverage']['transactions']
    assert len({r['report_id'] for r in observations})==len(observations)
    assert sum(yes(r['body_in_json']) for r in transactions)==archive['body_coverage']['body_present']
    for cohort,counts in archive['cohorts'].items():
        group=[r for r in observations if r['cohort']==cohort]
        assert len(group)==counts['reports']
        for k in ('decoded_carrier','script','fetch_and_relay','exact_oncb_endpoint','observed_output'):
            assert sum(yes(r[k]) for r in group)==counts[k]
    audit=json.loads((ROOT/'results/carrier-audit.json').read_text())
    records=audit['records'];counts=audit['counts']
    assert {r['report_id'] for r in records}=={r['report_id'] for r in observations if yes(r['decoded_carrier'])}
    assert counts['selected_reports']==len(observations)
    assert counts['decoded_carriers']==len(records)==7
    assert counts['carrier_digest_matches']==sum(r['decoded_sha256']==r['reported_sha256'] for r in records)==5
    assert counts['carrier_digest_mismatches']==sum(r['decoded_sha256']!=r['reported_sha256'] for r in records)==2
    assert counts['carriers_with_scripts']==sum(r['submitted_scripts']>0 for r in records)==5
    assert counts['carriers_with_matching_script']==sum(r['script_digest_matches']>0 for r in records)==3
    assert counts['oncb_target_request_records']==sum(bool(r['target_requests']) for r in records)==2
    assert counts['oncb_output_request_records']==sum(bool(r['output_requests']) for r in records)==1
    assert all(r['carrier_digest_matches']==(r['decoded_sha256']==r['reported_sha256']) for r in records)
    coverage=json.loads((ROOT/'results/transfer-coverage.json').read_text())
    members=[m for g in coverage['groups'] for m in g['members']]
    assert len(members)==len(set(members))==coverage['named_route_variants']==47
    assert set(members)=={c['id']+':'+route for c in cases.values() for route in c['routes']}
    assert len(coverage['groups'])==coverage['distinct_operational_configurations']==33
    print('PASS: experiment receipt outcomes and derived archive counts. Original archive source verification requires the pinned acquired JSON; this check does not replace it.')
if __name__=='__main__':main()
