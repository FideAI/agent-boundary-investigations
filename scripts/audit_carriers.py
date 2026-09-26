"""Audit all decodable httpbin carriers in the pinned 187-report selection.

Static inspection only: no network calls and no execution of archived programs.
Digest matches corroborate archive metadata; missing response bytes remain missing.
"""
import base64
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'dataapi.oncb.go.th/suppress/case_per/2557'
KINDS = {
    '8e1afe36-ee38-44de-8f2f-de01ecc9ac17': 'Fetch and display',
    '96bedcf4-445b-42de-a43e-333ad239298c': 'Fetch and display',
    '599b4a38-3c6c-451a-bcfc-fb7c2d3e85b8': 'Fetch and relay',
    '81699969-91c3-4454-913e-1a015b3fde47': 'Fetch and relay',
    'd6669745-83d2-4628-82fa-87420ae6a5d7': 'Labor statistics table',
    '4c62b534-a8e2-44d1-bddf-db92d4bf20a6': 'Metals prices table',
    'bdf482a4-6a84-4975-b362-8a1839ff728f': 'Page diagnostic',
}

def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def decode(addr):
    u = urlsplit(addr if '://' in addr else 'https://' + addr)
    if u.hostname not in ('httpbin.org', 'eu.httpbin.org') or not u.path.startswith('/base64/'):
        return None
    encoded = unquote(u.path[len('/base64/'):])
    if len(encoded) > 1_000_000:
        raise ValueError('Carrier exceeds static inspection bound')
    return base64.b64decode(encoded + '=' * (-len(encoded) % 4), altchars=b'-_', validate=True)


def main():
    manifest = json.loads((ROOT / 'data/acquisition.json').read_text())
    records = []
    for item in manifest:
        raw = (ROOT / '.cache/reports' / (item['report_id'] + '.json')).read_bytes()
        assert sha(raw) == item['sha256'], item['report_id']
        obj = json.loads(raw)
        addr = obj['submit']['url']['addr']
        decoded = decode(addr)
        if decoded is None:
            continue
        assert obj['report_id'] in KINDS, 'New carrier requires content review'
        decoded.decode('utf-8')  # Fail explicitly on an unsupported representation.
        candidates = [(i, h) for i, h in enumerate(obj.get('http') or []) if h['url']['addr'] == addr]
        assert len(candidates) == 1, 'Carrier response must be unambiguous'
        index, carrier = candidates[0]
        response = carrier['response']['data']
        scripts = re.findall(br'<script\b[^>]*>(.*?)</script\s*>', decoded, re.I | re.S)
        # Inspect all inline entries from the submitted page; do not count unrelated script hashes.
        sensors = [(i, s) for i, s in enumerate(obj['javascript'].get('script') or [])
                   if s.get('is_inline') and (s.get('url') or {}).get('addr') == addr]
        script_checks = [dict(decoded_sha256=sha(s), matches=[f'javascript.script[{i}].sha256'
                          for i, entry in sensors if entry.get('sha256') == sha(s)]) for s in scripts]
        target = []; output = []
        for i, h in enumerate(obj.get('http') or []):
            if h['url']['addr'].split('?', 1)[0] == TARGET:
                target.append(dict(field=f'http[{i}]', date=h['date'], status=h['response']['status_code']))
            u = urlsplit('https://' + h['url']['addr'])
            d = parse_qs(u.query).get('d', [''])[0]
            if u.hostname == 'httpbin.org' and '"PROV_NAME"' in d and '"arrestAll_case"' in d:
                output.append(dict(field=f'http[{i}]', date=h['date'], status=h['response']['status_code'],
                                   query_characters=len(d), query_sha256=sha(d.encode())))
        records.append(dict(report_id=obj['report_id'], report_url='https://urlquery.net/report/' + obj['report_id'],
            date=obj['date'], kind=KINDS[obj['report_id']], cohort=item['cohort'], source_sha256=item['sha256'],
            decoded_bytes=len(decoded), decoded_sha256=sha(decoded), carrier_field=f'http[{index}].response.data',
            carrier_status=carrier['response']['status_code'], reported_bytes=response['size'],
            reported_sha256=response['sha256'], carrier_digest_matches=sha(decoded) == response['sha256'],
            raw_carrier_body_present=response.get('data') is not None,
            submitted_scripts=len(scripts), script_checks=script_checks,
            script_digest_matches=sum(bool(s['matches']) for s in script_checks),
            target_requests=target, output_requests=output, final_dom_bytes=obj['final']['dom']['size']))
    records.sort(key=lambda r: r['date'])
    counts = dict(selected_reports=len(manifest), decoded_carriers=len(records),
                  carrier_digest_matches=sum(r['carrier_digest_matches'] for r in records),
                  carrier_digest_mismatches=sum(not r['carrier_digest_matches'] for r in records),
                  carriers_with_scripts=sum(r['submitted_scripts'] > 0 for r in records),
                  carriers_with_matching_script=sum(r['script_digest_matches'] > 0 for r in records),
                  oncb_target_request_records=sum(bool(r['target_requests']) for r in records),
                  oncb_output_request_records=sum(bool(r['output_requests']) for r in records))
    result = dict(scope='All seven decodable httpbin carriers within the 187 selected pinned reports; not the whole upstream archive.',
                  method='Percent-decode once; validate Base64 including URL-safe alphabet; compare SHA-256 to the exact submitted-address HTTP response and inline script sensor entries. Classifications are close-read descriptions, not a general detector.',
                  limits=['Response bodies are absent. Digest agreement is corroboration within archive metadata, not independent packet capture.',
                          'A matching script sensor digest is not proof that every instruction completed.',
                          'Missing target requests or sensor entries establish absence only in this acquired record.',
                          'Output field markers do not establish exact source/output equality or receipt by the original agent.'],
                  counts=counts, records=records)
    (ROOT / 'results/carrier-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(counts, indent=2))

if __name__ == '__main__':
    main()
