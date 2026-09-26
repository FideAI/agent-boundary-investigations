"""Describe repeated executable inputs without rerunning the local experiment."""
import ast
from collections import defaultdict
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def main():
    tree = ast.parse((ROOT / 'scripts/transfer_experiment.py').read_text())
    literals = {t.id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                for t in n.targets if isinstance(t, ast.Name) and t.id in ('FIXTURES', 'LABELS')}
    cases = json.loads((ROOT / 'data/transfer-cases.json').read_text())
    groups = defaultdict(list)
    for c in cases:
        for route in c['routes']:
            payload = literals['FIXTURES'][c['fixture']]
            signature = dict(payload_sha256=hashlib.sha256(payload).hexdigest(),
                label=literals['LABELS'].get(c['fixture']), destination=c['destination'],
                purpose=c['purpose'], grant=c['grant'], expected_authorized=c['expected_authorized'],
                route=route, **{k:bool(c.get(k, False)) for k in ('gate_outage','ack_lost','partial')})
            groups[json.dumps(signature, sort_keys=True)].append(c['id'] + ':' + route)
    result = dict(named_cases=len(cases), named_route_variants=sum(len(c['routes']) for c in cases),
        distinct_operational_configurations=len(groups),
        definition='Same payload bytes, resolved restriction label, recipient, purpose, supplied grant, scoring truth, route and injected faults. IDs, development/evaluation labels and unread narrative fields do not distinguish operational inputs.',
        limit='A descriptive grouping of this deterministic harness, not an independent-trial count or statistical population.',
        groups=[dict(inputs=json.loads(k), members=v) for k,v in groups.items()])
    (ROOT/'results/transfer-coverage.json').write_text(json.dumps(result,indent=2)+'\n')
    print({k:result[k] for k in ('named_cases','named_route_variants','distinct_operational_configurations')})

if __name__ == '__main__':main()
