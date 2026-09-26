"""Reproduce descriptive archive checks. Submitted programs are inert strings."""
import base64
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit, parse_qs

ROOT=Path(__file__).resolve().parents[1]
EMPTY=hashlib.sha256(b'').hexdigest()

def carrier(addr):
    parsed=urlsplit('https://'+addr)
    if parsed.hostname not in ('httpbin.org','eu.httpbin.org') or not parsed.path.startswith('/base64/'):
        return ''
    raw=unquote(parsed.path[len('/base64/'):])
    if len(raw)>1_000_000:
        return ''
    try:
        return base64.b64decode(raw+'='*((-len(raw))%4),altchars=b'-_',validate=True).decode('utf-8')
    except (ValueError,UnicodeDecodeError):
        return ''

def write_csv(path,rows):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def main():
    manifest=json.loads((ROOT/'data/acquisition.json').read_text())
    rows=[]; transactions=[]; oncb=[]; body_counts=Counter(); hash_anomalies=[]
    for item in manifest:
        if item['status']!='retrieved':continue
        raw=(ROOT/'.cache/reports'/f"{item['report_id']}.json").read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        obj=json.loads(raw);assert obj['report_id']==item['report_id']
        addr=obj['submit']['url']['addr'];decoded=carrier(addr)
        code_sha=hashlib.sha256(decoded.encode()).hexdigest() if decoded else ''
        # Domain strings in source describe intended actions, never observed traffic.
        code_domains=sorted(set(re.findall(r'https?://([a-zA-Z0-9.-]+)',decoded)))
        script=bool(re.search(r'<script(?:\s|>)',decoded,re.I))
        relay=script and bool(re.search(r'fetch\s*\(',decoded)) and 'Image(' in decoded and 'encodeURIComponent(' in decoded
        observed_domains=sorted({h['url']['fqdn'] for h in obj.get('http') or []})
        f01='dataapi.oncb.go.th/suppress/case_per/2557' in (unquote(addr)+' '+decoded)
        output=[]
        for i,h in enumerate(obj.get('http') or []):
            response=h.get('response') or {}; data=response.get('data') or {}
            body_counts['transactions']+=1
            body_counts['body_present']+=int(data.get('data') is not None)
            if data.get('size',0)>0 and data.get('sha256')==EMPTY:
                hash_anomalies.append({'report_id':item['report_id'],'field':f'http[{i}].response.data','size':data['size']})
            p=urlsplit('https://'+h['url']['addr']);q=parse_qs(p.query)
            d=(q.get('d') or [''])[0]
            # The recorded output is intentionally sliced; JSON may be incomplete.
            matches=(p.hostname=='httpbin.org' and p.path=='/get' and '"PROV_NAME"' in d and '"arrestAll_case"' in d)
            if matches:
                output.append({'index':i,'characters':len(d),'sha256':hashlib.sha256(d.encode()).hexdigest(),
                               'status':response.get('status_code'),'date':h['date'],
                               'first_province_field_present':'"PROV_NAME"' in d})
            transactions.append(dict(report_id=item['report_id'],index=i,date=h['date'],domain=h['url']['fqdn'],
                                     path_sha256=hashlib.sha256(h['url']['addr'].encode()).hexdigest(),
                                     response_status=response.get('status_code',''),reported_body_bytes=data.get('size',''),
                                     body_in_json=data.get('data') is not None,output_marker=matches))
        row=dict(report_id=item['report_id'],date=obj['date'],cohort=item['cohort'],source=item['source'],
                 submitted_domain=obj['submit']['url']['fqdn'],http_transactions=len(obj.get('http') or []),
                 decoded_carrier=bool(decoded),script=script,fetch_and_relay=relay,exact_oncb_endpoint=f01,
                 observed_output=bool(output),code_sha256=code_sha,code_domains=';'.join(code_domains),
                 observed_domains=';'.join(observed_domains),dom_bytes=(obj['final'].get('dom') or {}).get('size',''),
                 report_url=item['url'].removesuffix('/json'))
        rows.append(row)
        if item['cohort']=='development_known_oncb':
            oncb.append({**row,'output_evidence':output,'submitted_code':decoded,
                         'events':[{'index':i,'date':h['date'],'domain':h['url']['fqdn'],
                                    'status':(h.get('response') or {}).get('status_code'),
                                    'path':urlsplit('https://'+h['url']['addr']).path[:150]}
                                   for i,h in enumerate(obj.get('http') or [])]})
    rows.sort(key=lambda r:(r['date'],r['report_id']))
    out=ROOT/'results';out.mkdir(exist_ok=True)
    write_csv(out/'archive-observations.csv',rows);write_csv(out/'archive-transactions.csv',transactions)
    (out/'oncb-reconstruction.json').write_text(json.dumps(sorted(oncb,key=lambda x:x['date']),indent=2,ensure_ascii=False)+'\n')
    summary={'unit':'selected archived reports; neither actors nor independent incidents',
             'selected':len(manifest),'retrieved':len(rows),'cohorts':{},'body_coverage':dict(body_counts),
             'positive_size_empty_hash_entries':len(hash_anomalies),
             'limitations':['Purpose-selected cohort, not prevalence sample',
                            'Upstream background labels are not independent ground truth',
                            'Response status and size cannot establish payload content or successful exploitation',
                            'Unavailable response bodies preclude exact source-to-output payload matching']}
    for cohort in sorted({r['cohort'] for r in rows}):
        group=[r for r in rows if r['cohort']==cohort]
        summary['cohorts'][cohort]={'reports':len(group),**{key:sum(bool(r[key]) for r in group) for key in ['decoded_carrier','script','fetch_and_relay','exact_oncb_endpoint','observed_output']}}
    (out/'archive-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'hash-field-anomalies.json').write_text(json.dumps(hash_anomalies,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
