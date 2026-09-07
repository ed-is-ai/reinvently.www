"""Regression checks for the public evidence and subscription paths."""
import csv
import io
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import build_ed_o_meter as board

ROOT = Path(__file__).resolve().parent.parent


class PublicResearchTests(unittest.TestCase):
    def test_published_table_and_download_cover_the_roster(self):
        text = board.DATA_JS.read_text()
        models, source_run = board.parse_data_js(text)
        outputs = board.render_public_results(text)
        table = re.search(r'<tbody id="boardBody">(.*?)</tbody>', outputs[board.PAGE], re.S)[1]
        self.assertEqual(table.count('<tr>'), len(models))
        rows = list(csv.DictReader(io.StringIO(outputs[board.PAGE.parent / 'results.csv'])))
        self.assertEqual({r['name'] for r in rows}, {m['name'] for m in models})
        self.assertTrue(all(r['source_run'] == source_run for r in rows))
        self.assertTrue(all(r['methodology_url'].endswith('#scoring-title') for r in rows))

    def test_null_rubric_escaping_and_multiple_footnotes(self):
        models, run = board.parse_data_js(board.DATA_JS.read_text())
        model = {**models[0], 'name': '<model&>', 'rubric': None, 'pNote': [1, 3]}
        with patch.object(board, 'parse_data_js', return_value=([model], run)):
            output = board.render_public_results('fixture')[board.PAGE]
        table = re.search(r'<tbody id="boardBody">(.*?)</tbody>', output, re.S)[1]
        self.assertIn('&lt;model&amp;&gt;', table)
        self.assertIn('&#8212;', table)
        self.assertIn('<sup>1, 3</sup>', table)
        self.assertNotIn('<model&>', table)

    def test_updated_faqs_match_visible_answers(self):
        for slug in ('generative-ai-adoption-by-industry', 'uk-ai-policy-landscape-enterprise-2026'):
            text = (ROOT / f'blog/{slug}/index.html').read_text()
            objects = [json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)]
            faq = next(o for o in objects if o['@type'] == 'FAQPage')
            body = text.split('<body>', 1)[1]
            for question in faq['mainEntity']:
                self.assertIn(question['acceptedAnswer']['text'], body)
            self.assertNotIn('92 percent of global banks', text)

    def test_signup_uses_visible_provider_response(self):
        text = (ROOT / 'contact/index.html').read_text()
        self.assertIn('action="https://buttondown.com/api/emails/embed-subscribe/reinvently"', text)
        self.assertIn('newsletter_signup_attempt', text)
        self.assertNotIn('bd-frame', text)
        self.assertNotIn('setTimeout', text)
        self.assertNotIn("gtag('event', 'generate_lead'", text)


if __name__ == '__main__':
    unittest.main()
