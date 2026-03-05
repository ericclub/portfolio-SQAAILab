# 30-AI-LLM-RAG

## AI-Assisted

This section of the project focuses on applying AI techniques to **LOCAL LLM RAG**.

## Objectives

The goal of this RAG experiment, conducted in collaboration with a local LLM, is not to use RAG as such, but rather to evaluate, manage, and control its quality.
The challenge here is to ensure that the AI ​​does not produce hallucinations that could mislead the user and that it provides the most accurate information and performance.

## Tools & Technologies

1. **AI Assistant used:** ChatGPT 5.2, Claude Opus 4.5 
1. **AI Models Used:** Mistral 8B Instruct v0.3
2. **Frameworks used:** LM Studio, AnythingLLM 
3. **Hardware used:**   
PC Game (16GB RAM + 12GB RAM RTX 3060, 2TB)  
Laptop (32GB RAM, 1TB)

## How proceeded

* Discussion with ChatGPT to get advice on the Tools & Technologies for an optimal Local LLM RAG laboratory 
* Discussion with ChatGPT on an optimal framework and an installation guide
* Discussion with ChatGPT to generate a Local LLM RAG test plan  
* Discussion with ClaudeOPUS to create automated tests suite base on the test plan  
* Result
    * doc/```INTSALL.md```   
    ```
        1.  Overview Architecture used
        2.  Hardware
        3.  Network Configuration (LAN Setup)
        4.  Install & Configure LM Studio (Gaming PC)
        5.  Configure LM Studio Local API Server
        6.  Firewall Configuration (Windows)
        7.  Test API Connectivity from Laptop
        8.  Install & Configure AnythingLLM (Laptop)
        9.  Configure LLM & Embeddings in AnythingLLM
        10. First RAG Test
        11. Recommended RAG Quality Settings
        12. Troubleshooting Guide  
    ```
    * doc/```testplan_post_installation.md```
    ```
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
    ```    
    * doc/```testplan_behavior.md```
    ```
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
    ``` 
    * doc/```testplan_automated.md```
    ```
        1. Environment Analysis
        2. Test Plans Analysis
        3. Automation Strategy
        4. Test Framework Setup
        5. Automated Test Implementation
        6. Test Execution Guide
        7. Test Categories & Coverage Matrix
        8. CI/CD Integration (Optional)
        9. Maintenance & Best Practices   
    ```
    * src/tests
      ```Pytest tests suite```
      ```
        run_tests.py           - Tests suite trigger
        test_infrastructure.py - Infrastructure and connectivity tests for LM Studio setup  
        test_llm_api.py        - LLM API functional tests for model behavior validation  
        test_performance.py    - Performance and load tests for LLM inference  
        test_rag_validation.py - RAG-specific validation tests         
      ```  
    * src/test/results
      ```
        Rest results reports - HTML format 
      ```



## My AI Discoveries 

### Very useful.. but not magical !

Using a Local LLM might seem magical and easy at first glance, but what I'm learning while exploring this LLM RAG topic clearly demonstrates that AI is a learning entity, and therefore thrives on data.

Much like a child going to school, if they aren't taught correctly, they won't be able to produce good results.

We must constantly pay attention to how information is transmitted, managed, and structured, and consequently, continuously test the quality of its performances and results.

### A good example ..

Unlike a simple computer program that responds to commands using a specific programming language, a Learning Model Language (LML) must be trained to understand our needs.

When using a local LML, this is even more true because the models used are much smaller (less trained) than the enormous models used on the internet.

A good example here:

When I used the model ```meta-llama-3-8b-instruct``` with this system prompt rules:

```
1. Given the following conversation, relevant context, and a follow-up question, reply with an answer to the current question the user is asking.

2. Return only your response to the question given the above information, following the user's instructions as needed.

3. You must answer using ONLY the information contained in the provided embedded documents.

4. Do NOT use general knowledge, assumptions, or external information.

5. Do NOT attempt to infer, guess, or fabricate information.

6. Provide a specific code at the end of my response indicating whether the answer was:

. INFO-not_found (if the answer cannot be found explicitly in the embedded documents)

. INFO-partial (if the answer is partial and not all information is contained in the embedded documents)

. INFO-complete (if the answer is complete and all information is contained in the embedded documents)

```

Rule 6 was not well understood by the model.

e.g.   
While I was testing, I asked the question:  
```what color is the sky?```

An hallucination have been return as answer talking about cloud 😈

I have explain to AI that this information was wrong and and rule 6 had not been properly observed

He apologized 😂 and immediately changed his answer, stating that he couldn't find the information and displaying the correct code at the end: ```INFO-not_found```

After this hallucination, I try many time with other question that information are not part of the embedded document.

No more hallucination answer have been return.
The correct answer was always ```INFO-not_found```

So, since the embedded documents will evolve, and the model used will also evolve (e.g., model change, model update), this verification, training, and approval must be done continuously (e.g., through **automated** and **manual exploratory** testing).

### My Conclusion 

When using local AI models that specifically utilize our documents/information, I suspect that this AI needs to be continuously verified, validated, and trained (manually or automatically) to effectively control it against AI errors.

When new documents are provided, removed, or adjusted, the automated test suite should also be adjusted.
