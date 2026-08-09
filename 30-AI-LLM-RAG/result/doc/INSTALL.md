*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# Installation.md

**Configuration LLM local multi-machines + RAG**
LM Studio (PC Gaming) + AnythingLLM (Portable)


# Table des matières

1.  Aperçu de l'architecture utilisée
2.  Matériel
3.  Configuration réseau (configuration LAN)
4.  Installation et configuration de LM Studio (PC Gaming)
5.  Configuration du serveur API local LM Studio
6.  Configuration du pare-feu (Windows)
7.  Test de connectivité API depuis le portable
8.  Installation et configuration d'AnythingLLM (Portable)
9.  Configuration du LLM et des embeddings dans AnythingLLM
10. Premier test RAG
11. Paramètres RAG recommandés
12. Guide de dépannage


# 1. Aperçu de l'architecture utilisée

Cette configuration sépare le calcul et l'interface :

-   PC Gaming (RTX 3060 -- 12GB VRAM)
    -   Héberge LM Studio
    -   Exécute le modèle LLM
    -   Expose une API compatible OpenAI
-   Portable
    -   Héberge AnythingLLM
    -   Gère l'ingestion de documents (RAG)
    -   Se connecte à LM Studio via le LAN

Flux de communication :

Portable → AnythingLLM → API LM Studio (PC Gaming) → Réponse


# 2. Matériel / Logiciel

* PC Gaming : 
    * NVIDIA RTX 3060 (12GB VRAM) + 16GB RAM  
    * Windows 11
    * LM Studio

* Portable : 
    * 32GB RAM
    * Windows 11
    * AnythingLLM 
    
* Les deux machines connectées au même LAN


# 3. Configuration réseau (configuration LAN)

S'assurer : - Même sous-réseau (exemple 192.168.2.x) - Profil réseau privé -
Ping réussi

Test : ipconfig\
ping `<GamingPC_IP>`{=html}



# 4. Installation et configuration de LM Studio (PC Gaming)

Modèle recommandé : Mistral 8B Instruct 

Étapes : - Installer LM Studio - Télécharger le modèle - Charger le modèle
entièrement en mémoire



# 5. Configuration du serveur API local LM Studio

Paramètres du serveur local : Host : 0.0.0.0\
Port : 1234\
Mode : compatible OpenAI



# 6. Configuration du pare-feu

Autoriser le trafic TCP entrant sur le port 1234 (profil privé).



# 7. Test de connectivité API depuis le portable

Test du port : Test-NetConnection `<GamingPC_IP>`{=html} -Port 1234

Test de l'API : curl.exe http://`<GamingPC_IP>`{=html}:1234/v1/models



# 8. Installation et configuration d'AnythingLLM (Portable)

Installer AnythingLLM et le lancer.



# 9. Configuration du LLM et des embeddings dans AnythingLLM

LLM : URL de base : http://`<GamingPC_IP>`{=html}:1234/v1\
Modèle : mistralai/mistral-8b-instruct

Documents d'embeddings : voir context/doc/AnythingLLM_embedded_documents



# 10. Premier test RAG

Ajouter test.txt :

LM Studio s'exécute sur le PC Gaming avec Mistral 8B Instruct. Le GPU
est un RTX 3060 avec 12GB VRAM.

Demander : Où LM Studio s'exécute-t-il et quel modèle est utilisé ?



# 11. Paramètres RAG recommandés

Taille de chunk : 900\
Chevauchement : 120\
Top-K : 4\
Seuil de similarité : 0.35



# 12. Dépannage

-   Impossible de pinguer → Vérifier le réseau privé
-   Port inaccessible → Vérifier le pare-feu + LM Studio en cours d'exécution
-   Modèle manquant → S'assurer que le modèle est chargé

---

## 🇬🇧 English

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
