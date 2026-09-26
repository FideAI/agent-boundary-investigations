"""Reproduce in a disposable copy, preserving every released observation."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[1]

def main():
    if not shutil.which('curl'):
        raise SystemExit('curl is required. On Windows use WSL; native Windows is unverified.')
    if sys.flags.optimize:
        raise SystemExit('Run without -O.')
    baseline = json.loads((ROOT / 'results/transfer-summary.json').read_text())
    challenges = json.loads((ROOT / 'results/transfer-challenges.json').read_text())
    coverage = json.loads((ROOT / 'results/transfer-coverage.json').read_text())
    with tempfile.TemporaryDirectory(prefix='fide-transfer-reproduction-') as tmp:
        work = Path(tmp)
        for name in ('scripts', 'data', 'results'):
            shutil.copytree(ROOT / name, work / name, ignore=shutil.ignore_patterns('__pycache__'))
        for command in (['transfer_experiment.py', '--qualify'], ['transfer_experiment.py'], ['transfer_coverage.py'], ['verify_public.py']):
            run = subprocess.run([sys.executable, str(work / 'scripts' / command[0]), *command[1:]], cwd=work, capture_output=True, text=True, timeout=180)
            if run.returncode:
                print(run.stdout)
                print(run.stderr, file=sys.stderr)
                raise SystemExit(run.returncode)
            print('PASS:', ' '.join(command))
        rerun = json.loads((work / 'results/transfer-summary.json').read_text())
        for key in ('cases', 'route_variants', 'comparison_cells', 'conditions', 'script_sha256', 'cases_sha256'):
            assert rerun[key] == baseline[key], key
        assert json.loads((work / 'results/transfer-challenges.json').read_text()) == challenges
        assert json.loads((work / 'results/transfer-coverage.json').read_text()) == coverage
    print('PASS: functional results, challenges and coverage match. Frozen evidence was not overwritten; timing was not compared.')

if __name__ == '__main__':
    main()
