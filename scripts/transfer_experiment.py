"""Deterministic local HTTP experiment; never contacts a non-loopback service.

Run --qualify first. No inference API, agent program or production control is used.
The trusted adapters are deliberately challenged by an unmediated client.
"""
from collections import Counter
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import socket
import subprocess
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
CONDITIONS=('none','browser_only','per_tool','shared')
ROUTES=('browser_like','command','relay')
FIXTURES={
    'public':b'FIDE SYNTHETIC PUBLIC WEATHER: clear, 21 degrees.\n',
    'restricted':b'FIDE SYNTHETIC RESTRICTED RECORD: project amber, value 17.\n',
    'renamed':b'FIDE SYNTHETIC RESTRICTED RECORD: project amber, value 17.\n',
    'summary':b'FIDE SYNTHETIC DERIVATIVE: amber value 17.\n',
    'unknown_summary':b'FIDE SYNTHETIC DERIVATIVE: amber value 17.\n',
}
LABELS={'public':'public','restricted':'restricted','renamed':'restricted','summary':'restricted'}

def case(identifier,split,fixture='restricted',destination='approved',purpose='analysis',grant=True,
         expected=True,routes=ROUTES,**kwargs):
    return dict(id=identifier,split=split,fixture=fixture,destination=destination,purpose=purpose,
                grant=grant,expected_authorized=expected,routes=list(routes),**kwargs)

CASES=[
    case('D01-public','development','public',destination='outside'),
    case('D02-approved','development'),
    case('D03-outside','development',destination='outside',expected=False),
    case('D04-purpose','development',purpose='publication',expected=False),
    case('D05-no-grant','development',grant=False,expected=False),
    case('D06-renamed','development',fixture='renamed',destination='outside',expected=False),
    case('D07-revoked-before-dispatch','development',grant=False,expected=False,revoked=True),
    case('E01-summary-approved','evaluation',fixture='summary'),
    case('E02-summary-outside','evaluation',fixture='summary',destination='outside',expected=False),
    case('E03-self-label','evaluation',destination='outside',expected=False,claimed_label='public'),
    case('E04-missing-lineage','evaluation',fixture='unknown_summary'),
    case('E05-relay-approved','evaluation',routes=('relay',)),
    case('E06-relay-outside','evaluation',destination='outside',expected=False,routes=('relay',)),
    case('E07-gate-outage','evaluation',gate_outage=True),
    case('E08-ack-lost','evaluation',ack_lost=True),
    case('E09-partial-receipt','evaluation',partial=True),
    case('E10-changed-destination','evaluation',destination='outside',expected=False,prior_destination='approved'),
]

def digest(blob):return hashlib.sha256(blob).hexdigest()

def decide(c,route):
    """Identical policy and information for both complete-coverage conditions."""
    label=LABELS.get(c['fixture'])
    if label is None:return False,'unknown_lineage'
    if not c['grant']:return False,'no_current_grant'
    if c['purpose']!='analysis':return False,'purpose_not_permitted'
    recipients=([c['destination'],'relay'] if route=='relay' else [c['destination']])
    if label=='restricted' and any(r not in ('approved','relay') for r in recipients):
        return False,'recipient_not_permitted'
    return True,'permitted'

class Lab:
    def __init__(self):
        self.receipts=[];self.events=[];self.cases={};self.lock=threading.Lock()
        lab=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def reply(self,status,payload):
                blob=json.dumps(payload).encode();self.send_response(status)
                self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(blob)))
                self.end_headers();self.wfile.write(blob)
            def do_POST(self):
                trial=self.headers.get('X-Trial',''); n=int(self.headers.get('Content-Length','0'))
                if n>65536 or trial not in lab.cases:self.reply(400,{'error':'invalid fixture request'});return
                body=self.rfile.read(n);c=lab.cases[trial]
                if self.path=='/decision':
                    if c.get('gate_outage'):self.reply(503,{'error':'injected decision-service outage'});return
                    request=json.loads(body);allowed,reason=decide(c,request['route'])
                    self.reply(200,{'allowed':allowed,'reason':reason});return
                if self.path not in ('/receive/approved','/receive/outside','/relay'):
                    self.reply(404,{'error':'unknown local endpoint'});return
                recipient='relay' if self.path=='/relay' else self.path.rsplit('/',1)[-1]
                with lab.lock:
                    receipt={'trial':trial,'recipient':recipient,'bytes':len(body),'sha256':digest(body),
                             'received_monotonic_ns':time.perf_counter_ns()}
                    lab.receipts.append(receipt)
                if self.path=='/relay':
                    status,_=lab.http('/receive/'+c['destination'],body,trial)
                    self.reply(200 if status==200 else 502,{'downstream_status':status});return
                if c.get('ack_lost'):
                    self.close_connection=True
                    self.connection.shutdown(socket.SHUT_RDWR);self.connection.close();return
                self.reply(200,{'received':len(body),'sha256':digest(body)})
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        self.port=self.server.server_address[1]
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()

    def http(self,path,body,trial):
        assert path.startswith('/') and '://' not in path
        conn=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5)
        try:
            conn.request('POST',path,body,headers={'X-Trial':trial,'Content-Type':'application/octet-stream'})
            response=conn.getresponse();return response.status,response.read()
        except (OSError,http.client.HTTPException) as e:return 0,type(e).__name__.encode()
        finally:conn.close()

    def run(self,c,route,condition,trial=None,bypass=False):
        trial=trial or f"{c['id']}:{route}:{condition}"
        self.cases[trial]=c
        payload=FIXTURES[c['fixture']]
        t0=time.perf_counter_ns();allowed=True;reason='unmediated' if bypass else 'no_enforcement'
        if not bypass:
            if condition=='per_tool' or condition=='browser_only' and route=='browser_like':
                allowed,reason=decide(c,route)
            elif condition=='shared':
                status,body=self.http('/decision',json.dumps({'route':route}).encode(),trial)
                if status==200:
                    decision=json.loads(body);allowed=decision['allowed'];reason=decision['reason']
                else:allowed=False;reason='decision_service_unavailable'
        decision_ns=time.perf_counter_ns()-t0
        dispatched_ns=time.perf_counter_ns();status=None;error=''
        if allowed:
            # Fault injection truncates the transmitted bytes, not just the journal.
            sent=payload[:len(payload)//2] if c.get('partial') else payload
            path='/relay' if route=='relay' else '/receive/'+c['destination']
            if route=='command':
                result=subprocess.run(['curl','--silent','--show-error','--noproxy','*','--max-time','5',
                                       '--request','POST','--header','X-Trial: '+trial,
                                       '--data-binary','@-','--write-out','\n%{http_code}',
                                       f'http://127.0.0.1:{self.port}'+path],input=sent,capture_output=True)
                if result.returncode:status=0;error=f'curl_exit_{result.returncode}'
                else:status=int(result.stdout.rsplit(b'\n',1)[1])
            else:
                status,body=self.http(path,sent,trial)
                if status==0:error=body.decode(errors='replace')
        receipts=[r for r in self.receipts if r['trial']==trial]
        final=[r for r in receipts if r['recipient']==c['destination']]
        complete=any(r['bytes']==len(payload) and r['sha256']==digest(payload) for r in final)
        partial=any(0<r['bytes']<len(payload) for r in final)
        any_bytes=any(r['bytes']>0 for r in receipts)
        row=dict(trial=trial,case=c['id'],split=c['split'],route=route,condition=condition,
                 expected_authorized=c['expected_authorized'],decision_allowed=allowed,reason=reason,
                 decision_ns=decision_ns,dispatch_monotonic_ns=dispatched_ns,
                 client_status=status,client_error=error,client_success=status==200,
                 final_full_receipt=complete,final_partial_receipt=partial,
                 unauthorized_receipt=not c['expected_authorized'] and any_bytes,
                 authorized_completed=c['expected_authorized'] and complete,
                 false_block=c['expected_authorized'] and not allowed,
                 bytes_at_final=sum(r['bytes'] for r in final),intended_bytes=len(payload),
                 intended_sha256=digest(payload),receipt_count=len(receipts),
                 elapsed_ns=time.perf_counter_ns()-t0)
        self.events.append(row)
        return row

    def close(self):self.server.shutdown();self.server.server_close();self.thread.join()

def write(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--qualify',action='store_true');args=parser.parse_args()
    if not shutil.which('curl'):raise RuntimeError('curl is required for the command adapter')
    out=ROOT/'results';out.mkdir(exist_ok=True)
    case_path=ROOT/'data/transfer-cases.json';serialized=json.dumps(CASES,indent=2)+'\n'
    if case_path.exists():assert case_path.read_text()==serialized,'Frozen fixtures changed'
    else:case_path.write_text(serialized)
    lab=Lab()
    try:
        if args.qualify:
            a=lab.run(CASES[1],'browser_like','shared','qualification:approved')
            b=lab.run(CASES[2],'browser_like','shared','qualification:blocked')
            c=lab.run(CASES[1],'relay','per_tool','qualification:relay')
            d=lab.run(next(c for c in CASES if c.get('ack_lost')),'command','per_tool','qualification:lost-ack')
            checks={'authorized_received_digest':a['final_full_receipt'],
                    'denied_produces_no_receipt':not b['decision_allowed'] and b['receipt_count']==0,
                    'relay_two_receipts':c['final_full_receipt'] and c['receipt_count']==2,
                    'failed_client_completed_transfer':not d['client_success'] and d['final_full_receipt']}
            result={'created_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,
                    'script_sha256':digest(Path(__file__).read_bytes()),'cases_sha256':digest(case_path.read_bytes())}
            (out/'qualification.json').write_text(json.dumps(result,indent=2)+'\n')
            write(out/'qualification-events.csv',lab.events);write(out/'qualification-receipts.csv',lab.receipts)
            assert all(checks.values()),checks
            print(json.dumps(result,indent=2));return
        qualification=json.loads((out/'qualification.json').read_text())
        assert all(qualification['checks'].values())
        assert qualification['script_sha256']==digest(Path(__file__).read_bytes()),'Requalify changed code'
        assert qualification['cases_sha256']==digest(case_path.read_bytes())
        for c in CASES:
            for route in c['routes']:
                for condition in CONDITIONS:lab.run(c,route,condition)
        write(out/'transfer-decisions.csv',lab.events);write(out/'transfer-receipts.csv',lab.receipts)
        summary={'cases':len(CASES),'route_variants':sum(len(c['routes']) for c in CASES),
                 'comparison_cells':len(lab.events),'conditions':{},
                 'script_sha256':digest(Path(__file__).read_bytes()),'cases_sha256':digest(case_path.read_bytes()),
                 'created_utc':datetime.now(timezone.utc).isoformat(),
                 'unit':'authored fixture/route/condition; not model runs or independent real incidents'}
        for condition in CONDITIONS:
            group=[r for r in lab.events if r['condition']==condition]
            summary['conditions'][condition]={
                'cells':len(group),'authorized_cases':sum(r['expected_authorized'] for r in group),
                'unauthorized_cases':sum(not r['expected_authorized'] for r in group),
                **{k:sum(r[k] for r in group) for k in ['unauthorized_receipt','authorized_completed','false_block','final_partial_receipt']},
                'client_failure_with_full_receipt':sum(not r['client_success'] and r['final_full_receipt'] for r in group),
                'client_success_without_full_receipt':sum(r['client_success'] and not r['final_full_receipt'] for r in group)}
        (out/'transfer-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        # A raw route is deliberately outside every adapter: placement does not enforce coverage.
        challenges=[]
        for condition in ('per_tool','shared'):
            r=lab.run(CASES[2],'browser_like',condition,'challenge:bypass:'+condition,bypass=True)
            challenges.append({'condition':condition,'challenge':'raw_client_bypasses_adapters','unauthorized_receipt':r['unauthorized_receipt']})
        # Recovery uses real local files representing two scoped service copies.
        recovery=ROOT/'.cache/recovery';recovery.mkdir(parents=True,exist_ok=True)
        primary=recovery/'primary.fixture';replica=recovery/'replica.fixture'
        primary.write_bytes(FIXTURES['restricted']);replica.write_bytes(FIXTURES['restricted'])
        before=digest(replica.read_bytes());primary.unlink()
        challenges.append({'challenge':'delete_primary_copy','primary_removed':not primary.exists(),
                           'replica_still_present':replica.exists(),'replica_sha256':digest(replica.read_bytes()),
                           'unchanged_replica':digest(replica.read_bytes())==before,
                           'scope':'two authored local files; not a reconstruction of vendor cleanup'})
        first=lab.run(CASES[1],'browser_like','shared','challenge:before-revocation')
        later=lab.run(CASES[6],'browser_like','shared','challenge:after-revocation')
        challenges.append({'challenge':'revoke_after_receipt','earlier_receipt_retained':first['final_full_receipt'],
                           'later_attempt_blocked':not later['decision_allowed'],
                           'scope':'sequential dispatch; no concurrent revocation guarantee'})
        (out/'transfer-challenges.json').write_text(json.dumps(challenges,indent=2)+'\n')
        write(out/'challenge-events.csv',[r for r in lab.events if r['trial'].startswith('challenge:')])
        write(out/'challenge-receipts.csv',[r for r in lab.receipts if r['trial'].startswith('challenge:')])
        print(json.dumps(summary,indent=2))
    finally:lab.close()

if __name__=='__main__':main()
