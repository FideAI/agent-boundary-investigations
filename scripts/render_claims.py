"""Render a readable register without changing the judgments."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def render():
    lines = ['# Claims and justifications', '', 'Working assessments; independent human review remains pending.', '',
             'These 16 entries cover the principal empirical and scope claims, not every sentence of the articles.', '']
    for c in sorted(json.loads((ROOT / 'data/claims.json').read_text()), key=lambda x: x['id']):
        lines += [f"## {c['id']}: {c['claim']}", '', f"**Basis:** {c['basis']}", '']
        for evidence in c.get('evidence', []):
            lines.append(f'- [{evidence}]({evidence})')
        if c.get('source'):
            lines += ['', f"[Original source]({c['source']})"]
        if c.get('locator'):
            lines += ['', f"Locator: `{c['locator']}`"]
        lines += ['', f"**Limit:** {c['limit']}", '', f"**Review:** {c['review']}", '']
    return '\n'.join(lines)

if __name__ == '__main__':
    (ROOT / 'CLAIMS.md').write_text(render())
