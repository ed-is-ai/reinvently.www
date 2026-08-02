# House prose rules

Vale styles used by `.github/workflows/prose.yml`. Everything here is
**advisory** — the job annotates a pull request and never fails it.

Run them locally with:

```sh
vale blog/*/index.html          # everything
vale blog/rag-vs-graphrag/      # one post
```

| Rule | What it catches | Level |
|---|---|---|
| `AIPhrases` | Stock LLM phrasing — `delve into`, `cutting-edge`, `in today's fast-paced…` | warning |
| `Wordiness` | Padding with a shorter equivalent — `in order to` → `to` | suggestion |
| `Epigrams` | More than two `not X, but Y` antitheses in one post | warning |
| `ServicePitch` | CTAs that sell services instead of asking for a blog subscription | warning |
| `Readability` | Flesch-Kincaid grade above 14 for the post as a whole | suggestion |

## Two things to know before editing these

**Quoted material is exempt.** Every rule carries `scope: ~blockquote`, because
the house style reproduces statistics and adversarial prompts verbatim. A linter
nudging you to reword someone else's words is worse than useless. Note that
`BlockIgnores` in `.vale.ini` does *not* apply to HTML — scoping is the
mechanism that works.

**`substitution` messages take the replacement first.** Vale passes the
suggested word as the first `%s` and the matched text as the second, so
`message: "Use '%s' instead of '%s'."` reads correctly and the obvious ordering
does not.

## Calibration

Measured across the 27 posts as of August 2026, these rules produce 12 alerts
in total — mostly readability on the longest posts, plus a handful of wordiness
hits. That ratio is the point. If a rule starts firing on every post it has
stopped carrying information, and the fix is to change the rule rather than to
work around it.
