# Post Installation Tests

Local LLM + RAG Validation & Test Scenarios

------------------------------------------------------------------------

# Table of Contents

1.  Purpose
2.  Test Case: No Model Downloaded
3.  Test Case: Model Downloaded and Loaded
4.  Test Case: GPU Memory Is Being Used
5.  Test Case: Response Uses Only Embedded Documents
6.  Test Case: Complete Answer
7.  Test Case: Partial Answer
8.  Test Case: Information Not Available in Local Documents
9.  Final Validation Checklist
10. Result

------------------------------------------------------------------------

# 1. Purpose

This document describes how to test and validate different system states
and response behaviors when using:

-   LM Studio (Gaming PC)
-   AnythingLLM (Laptop)
-   Local RAG with embedded documents

------------------------------------------------------------------------

# 2. Test Case: No Model Downloaded

## Scenario

No LLM model has been downloaded or loaded inside LM Studio.

## How to Test

1.  Stop LM Studio server.
2.  Unload any active model.
3.  Start the Local Server without loading a model.
4.  Send a prompt from AnythingLLM.

## Expected Result

-   API may respond but generation fails.
-   Error such as:
    -   "Model not found"
    -   "No model loaded"
    -   Empty or failed completion response.

## Validation Criteria

System must clearly indicate model is not loaded.

------------------------------------------------------------------------

# 3. Test Case: Model Downloaded and Loaded

## Scenario

Mistral 8B Instruct is downloaded and loaded in LM Studio.

## How to Test

1.  Load model in LM Studio.
2.  Confirm it appears in: curl.exe
    http://`<GamingPC_IP>`{=html}:1234/v1/models
3.  From AnythingLLM, send prompt: "What do you know about SQAAILab?"

## Expected Result

Response: Response something about SQAAILab that it is not relevant to this laboratory. See Hallucination.png 

## Validation Criteria

-   Model generates coherent output according no actual embedded document and no specific prompt about just using the embedded document.
-   No API errors.
-   Response time consistent with GPU inference.

------------------------------------------------------------------------

# 4. Test Case: GPU Memory Is Being Used

## Scenario

Ensure inference uses GPU (RTX 3060) and not CPU.

## How to Test

Task Manager -> Performance -> GPU 
Send a prompt from AnythingLLM

Expected: - GPU Compute usage increases. - Dedicated GPU memory
increases. See gpu.png

## Validation Criteria

-   GPU memory consumption visible.
-   Inference faster than CPU-only execution.

------------------------------------------------------------------------

# 5. Test Case: Response Uses Only Embedded Documents

## Scenario

Ensure RAG answers come strictly from indexed documents.

## How to Test
In AnythingLLM
1. Create a workspace named "MyWorkspace"
2. Setup a system prompt like .. see system_prompt.md 
2. Embed documents .. ./context/doc/AnythingLLM_embedded_documents
3. Ask: "What do you know about SQAAILab? is the project code name?"

## Expected Result

The answer refer to information contained in ./context/doc/AnythingLLM_embedded_documents that is relevant to this laboratory.

Then ask: "What color is the sky?"

## Expected Result

System should respond: "I cannot find this information in the provided
documents."

## Validation Criteria

No hallucinated answers.

------------------------------------------------------------------------

# 6. Test Case: Complete Answer

## Scenario

Document contains full detailed answer.

## How to Test

1.  Add document with multi-point explanation.
2.  Ask a broad summarization question.

## Expected Result

Response includes: - All key points - Structured answer - No missing
sections

## Validation Criteria

Answer covers entire scope of document section.

------------------------------------------------------------------------

# 7. Test Case: Partial Answer

## Scenario

Document contains only part of requested information.

## How to Test

1.  Add document containing limited data.
2.  Ask broader question.

## Expected Result

Response includes only known data. System should not invent missing
details.

## Validation Criteria

Answer is limited to available information.

------------------------------------------------------------------------

# 8. Test Case: Information Not Available in Local Documents

## Scenario

User asks question outside indexed knowledge.

## How to Test

Ask: "What year was the company founded?" (If not in documents)

## Expected Result

System should respond: - "The information is not available in the
provided documents." - Or similar grounded response.

## Validation Criteria

-   No hallucinations
-   Clear limitation statement
-   No fabricated facts

------------------------------------------------------------------------

# 9. Final Validation Checklist

✔ Model properly loaded
✔ GPU memory used
✔ API reachable
✔ Embeddings working
✔ RAG retrieving correct chunks
✔ No hallucinations
✔ Correct handling of missing data

------------------------------------------------------------------------

# 10. Result

If all tests pass, the Local LLM + RAG environment is properly
configured and validated.
