# Prompt experiment evidence

## Status

The original baseline was run on 2026-09-15 with Gemini `gemini-3.5-flash`.
The saved JSON is unmodified evaluator output, including provider errors.
It measured 21/30 cases and is **not a valid full-suite baseline**.
The API reported 5 requests/minute and 20 requests/day free-tier limits.
The observed partial accuracy must not be used as a before/after metric.

`prompts/system_prompt_v0.md` preserves the original bytes. v1, v2 and v3 are
successive prompt drafts, **not evaluated versions**. The active artifact matches
the v3 draft. Keep all snapshots so the original baseline can still be rerun.
See REPORT.md B2 for five trace findings and the distinction between automatic
failures, manual findings and provider errors.

## Reproduce after sufficient quota is available

Run from `starter_v0`, using its Python 3.11 virtual environment and local `.env`.
Do not print or commit API keys. Keep the same model, tool declarations, dataset
and temperature (the agent fixes temperature at 0.0) across all versions.

```powershell
.\.venv\Scripts\python.exe run_eval.py --provider gemini --model gemini-3.5-flash --version v0 --suite base --eval-cases data/eval_base.json --system-prompt runs/prompts/system_prompt_v0.md
.\.venv\Scripts\python.exe run_eval.py --provider gemini --model gemini-3.5-flash --version v1 --suite base --eval-cases data/eval_base.json --system-prompt runs/prompts/system_prompt_v1.md
.\.venv\Scripts\python.exe run_eval.py --provider gemini --model gemini-3.5-flash --version v2 --suite base --eval-cases data/eval_base.json --system-prompt runs/prompts/system_prompt_v2.md
.\.venv\Scripts\python.exe run_eval.py --provider gemini --model gemini-3.5-flash --version v3 --suite base --eval-cases data/eval_base.json --system-prompt runs/prompts/system_prompt_v3.md
```

These commands do not implement rate limiting. Ensure the project has sufficient
daily and per-minute quota before rerunning. If a different model is selected,
rerun all four versions with that same model; do not compare across models.
Review each result before deciding whether the next draft should be revised.
Never overwrite or merge runs to hide provider failures.

Only populate accuracy comparisons when `provider_error_cases == 0` and
`measured_cases == total_cases == 30`, after reviewing tool results as well.
The CSV currently records planned hypotheses and snapshot hashes; blank metrics
mean unmeasured/invalid, and a blank run_file means no evaluation was performed.
