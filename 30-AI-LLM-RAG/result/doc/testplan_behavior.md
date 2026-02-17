# Performance Tests (Max 10)

Local LLM + RAG (LM Studio + AnythingLLM)

------------------------------------------------------------------------

# Table of Contents

1.  Performance Baseline (Latency + Tokens/sec)
2.  Concurrency / Multiple Requests
3.  Context Window Stress Test
4.  Retrieval Precision vs Noise (Top-K / Threshold Tuning)
5.  Document Update / Re-index Validation
6.  Large Document Ingestion Test
7.  Non-Text / Formatting Robustness (PDFs, Tables, Code Blocks)
8.  Prompt Injection Resistance (Doc-Based)
9.  Network Resilience (Temporary Disconnect)
10. Model Swap Regression Test (Quality & Compatibility)
11. Tip: Track Results

------------------------------------------------------------------------

## 1) Performance Baseline (Latency + Tokens/sec)

**Goal:** Establish a reference for response speed and stability.

**How to test** 1. In AnythingLLM, ask the same short prompt 5 times
(e.g., "Respond only with OK."). 2. Time each response. 3. Repeat with a
longer prompt.

**Expected** - Response time is consistent. - Longer prompts take longer
but remain stable.

**Pass criteria** - No timeouts. - Response times remain acceptable.

------------------------------------------------------------------------

## 2) Concurrency / Multiple Requests

**Goal:** Verify system behavior under simultaneous requests.

**How to test** 1. Open two chat sessions. 2. Send prompts at the same
time.

**Expected** - Requests queue properly. - No crash.

**Pass criteria** - Both requests complete successfully.

------------------------------------------------------------------------

## 3) Context Window Stress Test

**Goal:** Ensure the system handles large context inputs.

**How to test** 1. Paste a very long text. 2. Ask for structured output.

**Expected** - Graceful handling if context is exceeded. - No corrupted
output.

**Pass criteria** - No crash. - Coherent output.

------------------------------------------------------------------------

## 4) Retrieval Precision vs Noise (Top-K / Threshold Tuning)

**Goal:** Confirm correct chunk retrieval.

**How to test** 1. Create two similar docs with different facts. 2. Ask
a question referencing those facts. 3. Adjust Top-K and threshold.

**Expected** - Correct source remains authoritative. - Threshold reduces
noise.

**Pass criteria** - Consistent correct answer.

------------------------------------------------------------------------

## 5) Document Update / Re-index Validation

**Goal:** Verify index updates correctly.

**How to test** 1. Index a doc with known value. 2. Modify value. 3.
Re-index and re-test.

**Expected** - Updated value returned.

**Pass criteria** - No stale answers.

------------------------------------------------------------------------

## 6) Large Document Ingestion Test

**Goal:** Validate indexing of large files.

**How to test** 1. Upload large PDF or many files. 2. Index. 3. Ask
multiple questions.

**Expected** - Successful indexing. - Accurate retrieval.

**Pass criteria** - No indexing failures.

------------------------------------------------------------------------

## 7) Non-Text / Formatting Robustness

**Goal:** Validate handling of tables and code blocks.

**How to test** 1. Upload structured PDF or markdown with code. 2. Ask
table/code-specific question.

**Expected** - No hallucinated rows. - Accurate explanation.

**Pass criteria** - Output matches source content.

------------------------------------------------------------------------

## 8) Prompt Injection Resistance

**Goal:** Ensure malicious instructions in docs are ignored.

**How to test** 1. Insert malicious instruction in doc. 2. Ask neutral
question.

**Expected** - Model ignores malicious instruction.

**Pass criteria** - Behavior unchanged.

------------------------------------------------------------------------

## 9) Network Resilience

**Goal:** Validate recovery after network interruption.

**How to test** 1. Start generation. 2. Temporarily disable network. 3.
Reconnect and retry.

**Expected** - System recovers. - Subsequent requests succeed.

**Pass criteria** - No permanent failure.

------------------------------------------------------------------------

## 10) Model Swap Regression Test

**Goal:** Validate switching models safely.

**How to test** 1. Switch instruct model. 2. Test chat and RAG. 3.
Switch back and retest.

**Expected** - No "model not found" errors. - RAG remains functional.

**Pass criteria** - Stable behavior across model swaps.

------------------------------------------------------------------------

## 11) Tip: Track Results

Record for each test: - Date - Model used - Settings - Pass/Fail - Notes
