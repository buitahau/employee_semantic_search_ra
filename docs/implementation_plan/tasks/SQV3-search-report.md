# Search Quality Report

**Phase:** Search Quality Validation  
**Status:** todo

---

## Description

The test prompts from SQV2 need to be executed against the live search pipeline and their actual results compared to the expected results. Without an automated runner and a structured report, quality regressions go undetected and there is no baseline to compare against after pipeline changes.

This task implements a test runner that loads the SQV2 prompt file, executes each query against the search pipeline, collects the actual response, and evaluates it against the expected outcome. Evaluation checks response type match, whether the expected top employee appears in the actual results and at what rank, and whether the top score meets the minimum threshold. The runner then generates a comparison report that clearly shows passed, failed, and borderline cases, along with the actual vs expected values for each failure.

The report format should be human-readable (Markdown or HTML) so it can be reviewed in a PR or shared with the team, and machine-readable (JSON) so it can be diffed across runs to track improvement over time.

---

## Deliverables Checklist

- [ ] Test runner script created at `tests/search_quality/run.py` that loads the SQV2 prompt file and executes each query against the search pipeline
- [ ] Each result evaluated on: response type match, expected employee rank in results, and min score threshold
- [ ] Comparison report generated in Markdown (human-readable) and JSON (machine-readable) after each run
- [ ] Report clearly distinguishes passed, failed, and borderline (score within 10% of threshold) cases
- [ ] Each failure row shows actual vs expected values for easy diagnosis
- [ ] Runner exits with a non-zero code if any prompt fails, so it can be gated in CI
- [ ] Instructions for running the suite added to the project README or `tests/search_quality/README.md`
