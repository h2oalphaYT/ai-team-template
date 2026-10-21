---
name: ai-ml-engineering
description: Workflow for AI and ML tasks, including machine learning, deep learning, computer vision, NLP, LLM features, prompts, RAG and embeddings, data pipelines, training, evaluation and inference. Use when building, changing, evaluating, debugging or serving a model or data pipeline. Requires data validation, reproducibility, suitable metrics and truthful experiment reporting; never invents results.
argument-hint: "<AI/ML task>"
---

# AI/ML Engineering

Task: $ARGUMENTS

Use with the `/execute-task` lifecycle and report. Delegate the technical work to the
`ai-ml-engineer` agent, which holds the detailed method; this skill defines the gates and the
required evidence.

**Use when:** the task involves a model, prompt, dataset, embedding, retrieval, training,
evaluation, or inference. **Do not use** for ordinary application code that merely calls an
existing, unchanged AI endpoint; use `/feature-development` or `/bug-fix`.

## Gate 1: use case and inventory (before choosing anything)

- Define the prediction or output, its consumer, the cost of each error type, and latency and
  cost limits.
- Inspect what exists: ML frameworks in manifests, notebooks, training scripts, datasets (by
  path and size only), model artefacts, serving code, hardware notes. Follow the existing stack.
- Confirm whether ML is needed at all; a rules or search baseline may be enough.

## Gate 2: data

Report provenance and licence, presence of personal data, quality issues, class balance,
and leakage checks. Define the train/validation/test split strategy. **Do not send private
data to external APIs or services without owner approval.**

## Gate 3: plan and approval

Write a plan (task-plan template) that names the baseline, candidate approaches, metrics,
evaluation dataset, compute needs, and expected cost. **Owner approval is required** before
long or costly training runs, paid API usage at scale, new heavyweight dependencies
(PyTorch, TensorFlow, CUDA images), or uploading data or models anywhere.

## Gate 4: reproducible experiments

- Fix seeds, pin versions, record config, data snapshot identifiers, hardware, and the exact
  command for every run.
- Evaluate the baseline and candidates on the same held-out data. Report quality metrics,
  latency (p50/p95), memory, and cost.
- Include failure-case analysis, robustness checks, and bias across relevant groups when people
  are affected.

## Gate 5: integration and tests

Add tests for preprocessing, input/output contracts, inference shape and range, golden
examples, and API integration. For LLM features: treat model output as untrusted, validate it
before use, guard against prompt injection from user and retrieved content, and set timeouts
and fallbacks. Run the tests and report results.

## Truthful reporting (mandatory)

- Report only metrics that were computed in this session or that exist in committed, cited
  artefacts. Say which.
- If training or evaluation could not run (no GPU, no data access, time), state that clearly
  and give the command the owner can run. Never estimate a metric and present it as measured.
- Never claim a model was trained, fine-tuned, or improved without evidence.

## Output additions to the delivery report

```
## Experiment log
| Run | Model/config | Data split | Metric(s) | Latency | Command | Status (ran / not run) |
## Data notes (provenance, quality, leakage checks)
## Limitations and failure cases
## Model card / documentation updated: yes/no (path)
```

## Example invocations

```
/ai-ml-engineering Evaluate the image classification pipeline
/ai-ml-engineering Add RAG over our product docs with citations
/ai-ml-engineering Check the churn dataset for leakage and class imbalance
```
