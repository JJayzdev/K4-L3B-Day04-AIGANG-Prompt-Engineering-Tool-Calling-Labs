# Evaluation evidence

OpenRouter experiment: same model `openai/gpt-4o-mini`, tools and base dataset.
Use the selected run links in REPORT.md B2 and provider-specific rows in version_log.csv.
The original CSV rows describe the earlier incomplete Gemini experiment and unevaluated drafts.
`prompts/system_prompt_v*.md` are historical Gemini drafts.
`prompts/openrouter_v*.md` preserve the actual OpenRouter revisions byte-for-byte.
Run labels alone do not select prompts; verify prompt_hash and tools_hash.
Repeated v0/v1/v2/v3 labels with identical artifact hashes are repetitions, not improvements.
Connection-error runs and the partial Gemini quota-error run are not score evidence.

Reproduce an actual revision from starter_v0 (replace N with the desired revision):

```powershell
python run_eval.py --provider openrouter --model openai/gpt-4o-mini --version vN --suite base --eval-cases data/eval_base.json --system-prompt runs/prompts/openrouter_vN.md
```

Review full coverage, provider errors, individual regressions and tool results before claiming improvement.
