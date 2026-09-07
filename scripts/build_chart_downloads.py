#!/usr/bin/env python3
"""Export the global-adoption article's inline charts with source attribution.

Run after changing those charts. --check verifies the committed downloads.
"""
import argparse
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'blog/global-ai-adoption-attitudes/index.html'
URL = 'https://reinvently.co.uk/blog/global-ai-adoption-attitudes/'


def downloads():
    source = PAGE.read_text(encoding='utf-8')
    modified = re.search(r'"dateModified"\s*:\s*"([^"]+)"', source)[1]
    outputs = {}
    for svg in re.findall(r'<svg\b.*?</svg>', source, flags=re.S):
        root = ET.fromstring(svg)
        title = root.find('{http://www.w3.org/2000/svg}title')
        if title is None or title.get('id') not in ('country-chart-title', 'gap-chart-title'):
            continue
        name = title.get('id').removesuffix('-title')
        _, _, width, height = map(int, root.get('viewBox').split())
        inner = svg[svg.index('>') + 1:svg.rindex('</svg>')]
        outputs[ROOT / f'images/research/{name}.svg'] = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height + 96}" '
            f'role="img" aria-labelledby="export-title">\n'
            f'<title id="export-title">{escape(title.text)}</title>\n'
            f'<metadata>Source: Microsoft AI Diffusion Index. Presentation: Reinvently. '
            f'Article: {URL} Article modified: {escape(modified)}. '
            'Population estimates are not measures of productivity or enterprise ROI.</metadata>\n'
            '<rect width="100%" height="100%" fill="#111"/>\n'
            f'<text x="16" y="24" fill="#e2e2e2" font-family="sans-serif" font-size="15">{escape(title.text)}</text>\n'
            f'<svg x="0" y="36" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{inner}</svg>\n'
            f'<text x="16" y="{height + 55}" fill="#aaa" font-family="sans-serif" font-size="11">'
            'Source: Microsoft AI Diffusion Index. People aged 15–64; not enterprise adoption or ROI.</text>\n'
            f'<a href="{URL}"><text x="16" y="{height + 75}" fill="#aaa" font-family="sans-serif" font-size="10">'
            f'Reinvently | {URL}</text></a>\n</svg>\n'
        )
    if len(outputs) != 2:
        raise ValueError('Expected both labelled adoption charts')
    for content in outputs.values():
        ET.fromstring(content)
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for path, content in downloads().items():
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    if stale:
        raise SystemExit('Stale chart downloads: ' + ', '.join(stale))
    print('Both chart downloads match the article.')
