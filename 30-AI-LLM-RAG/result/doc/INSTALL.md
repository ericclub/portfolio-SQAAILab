# Installation.md

**Multi-Machine Local LLM + RAG Setup**
LM Studio (Gaming PC) + AnythingLLM (Laptop)


# Table of Contents

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


# 1. Overview Architecture Used

This setup separates compute and interface:

-   Gaming PC (RTX 3060 -- 12GB VRAM)
    -   Hosts LM Studio
    -   Runs the LLM model
    -   Exposes OpenAI-compatible API
-   Laptop
    -   Hosts AnythingLLM
    -   Handles document ingestion (RAG)
    -   Connects to LM Studio over LAN

Communication Flow:

Laptop → AnythingLLM → LM Studio API (Gaming PC) → Response


# 2. Hardware / Software

* Gaming PC: 
    * NVIDIA RTX 3060 (12GB VRAM) + 16GB RAM  
    * Windows 11
    * LM Studio

* Laptop: 
    * 32GB RAM
    * Windows 11
    * AnythingLLM 
    
* Both machines connected to the same LAN


# 3. Network Configuration (LAN Setup)

Ensure: - Same subnet (example 192.168.2.x) - Private network profile -
Ping successful

Test: ipconfig\
ping `<GamingPC_IP>`{=html}



# 4. Install & Configure LM Studio (Gaming PC)

Recommended Model: Mistral 8B Instruct 

Steps: - Install LM Studio - Download model - Load model fully into
memory



# 5. Configure LM Studio Local API Server

Local Server settings: Host: 0.0.0.0\
Port: 1234\
Mode: OpenAI Compatible



# 6. Firewall Configuration

Allow inbound TCP port 1234 (Private profile).



# 7. Test API Connectivity from Laptop

Test port: Test-NetConnection `<GamingPC_IP>`{=html} -Port 1234

Test API: curl.exe http://`<GamingPC_IP>`{=html}:1234/v1/models



# 8. Install & Configure AnythingLLM (Laptop)

Install AnythingLLM and launch.



# 9. Configure LLM & Embeddings in AnythingLLM

LLM: Base URL: http://`<GamingPC_IP>`{=html}:1234/v1\
Model: mistralai/mistral-8b-instruct

Embeddings documents: See context/doc/AnythingLLM_embedded_documents



# 10. First RAG Test

Add test.txt:

LM Studio runs on the Gaming PC using Mistral 8B Instruct. The GPU
is an RTX 3060 with 12GB VRAM.

Ask: Where is LM Studio running and which model is used?



# 11. Recommended RAG Settings

Chunk Size: 900\
Overlap: 120\
Top-K: 4\
Similarity Threshold: 0.35



# 12. Troubleshooting

-   Cannot ping → Check Private network
-   Port unreachable → Check firewall + LM Studio running
-   Model missing → Ensure model is loaded
