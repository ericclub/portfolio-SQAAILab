![alt text](SQAAILab_small.png)
# SQAAILab
> _Laboratoire d'Assurance Qualité Logicielle et d'Intelligence Artificielle_

*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

### Aperçu du projet

Ce projet explore comment l'**Intelligence Artificielle (IA)** peut améliorer les pratiques d'**Assurance Qualité Logicielle (AQL)**.

Voici la structure de base du projet
```
portfolio-SQAAILab          Racine du laboratoire
│
├ nn-AI-topic-name          Racine d'un sujet IA
│   │
│   ├ context               Information fournie à l'IA pour générer le résultat
│   ├ result
│   │   ├ doc               Documentation générée par l'IA concernant le résultat
│   │   ├ src               Code généré par l'IA concernant le résultat
│   │
│   ├ nn-README.md          Information générale sur ce sujet d'exploration
│   │
│
├ README.md                 Information générale sur ce projet portfolio-SQAAILab
│
```

Chaque sous-dossier se concentre sur une approche spécifique pilotée par l'IA.  
Merci de consulter chaque fichier **nn-README.md** pour des explications, exemples et workflows détaillés.

🚀 **Vision :**   
Les sujets listés ci-dessous représentent les domaines d'exploration actuels. Ce dépôt est conçu comme un laboratoire vivant pour l'IA appliquée à l'Assurance Qualité Logicielle et évoluera continuellement pour expérimenter, valider et documenter les techniques, outils et paradigmes émergents pilotés par l'IA à mesure que le domaine mûrit.

### Sujets couverts

#### 🔹 Vibe Coding
10-AI-vibe-coding

Une approche de développement pilotée par l'IA où les développeurs utilisent des prompts en langage naturel pour guider des modèles d'IA générative (comme les LLM) afin de générer, affiner et déboguer du code.

#### 🔹 Documentation inversée
15-AI-doc-generation

Une approche analytique qui exploite le code source existant pour recréer des spécifications manquantes, obsolètes ou non documentées.

#### 🔹 BDD génératif
20-AI-QA-analysis-assistant

Une approche assistée par IA du **Behavior-Driven Development (BDD)** qui automatise la génération de scénarios BDD, de définitions d'étapes et de scripts de test. Les exigences en langage naturel sont transformées en syntaxe **Gherkin (Given–When–Then)** structurée, ce qui améliore la couverture de test, réduit l'effort manuel et augmente la cohérence tout au long du cycle de vie du développement logiciel.

#### 🔹 Conception de tests générée par IA  
20-AI-QA-analysis-assistant

Dérivation automatique de cas de test, de cas limites et d'idées de tests exploratoires à partir du code source, des user stories, des API et du comportement du système.

#### 🔹 Tests en Vibe Coding  
25-AI-vibe-coding-tests

C'est la tendance majeure actuellement. Plutôt que de se soucier d'une syntaxe de code stricte, le testeur se concentre sur l'intention (le « vibe ») et laisse l'IA (comme les LLM) générer le code d'automatisation. Cela permet de créer des suites de tests complexes simplement en décrivant le scénario en langage naturel.

#### 🔹 LLM RAG
30-AI-LLM-RAG  

« Large Language Model » avec « Retrieval-Augmented Generation » - Consulter une base de connaissances faisant autorité, externe aux données d'entraînement de l'IA, avant de générer une réponse en utilisant des informations spécifiques ou sensibles telles que des documents locaux, des bases de données, des pages web, des notes personnelles, etc.

---
### 🔮 Domaines d'exploration futurs

À mesure que ce projet évolue, il vise à explorer un éventail plus large de capacités pilotées par l'IA à travers le cycle de vie de l'Assurance Qualité Logicielle, incluant (sans s'y limiter) :

#### 🔹 Tests autonomes / agentiques
Des agents qui planifient, exécutent, diagnostiquent et adaptent de manière autonome des suites de tests (y compris l'auto-réparation) tout au long du cycle de vie de l'AQL avec une intervention humaine minimale (une partie est déjà couverte sous « Tests en Vibe Coding »).

#### 🔹 Model Context Protocol (MCP) pour l'outillage QA
Standardiser la manière dont les agents IA se connectent aux outils de test, sources de données, environnements et systèmes CI/CD via un protocole commun.

#### 🔹 Ingénierie de contexte
Concevoir, sélectionner et gérer délibérément ce qu'un agent IA voit à chaque étape — mémoire, documents récupérés, sorties d'outils, historique de conversation — pour maintenir la performance à mesure que le contexte grandit. Va au-delà du RAG de base vers la récupération agentique et l'assemblage de contexte multi-source pour les tâches QA.

#### 🔹 Orchestration QA multi-agents
Coordonner des équipes d'agents IA spécialisés (par exemple, un qui révise les changements de code, un qui génère des données de test, un qui exécute et analyse les résultats) travaillant en parallèle à travers le cycle de vie de l'AQL, plutôt que de s'appuyer sur un seul agent généraliste.

#### 🔹 Génération intelligente de données de test  
Créer des données de test réalistes, conformes et centrées sur des scénarios à l'aide de l'IA générative et de techniques de données synthétiques.

#### 🔹 Détection de bugs et analyse de cause racine assistées par IA  
Exploiter l'IA pour analyser les logs, traces, résultats de tests et changements de code afin d'identifier proactivement les défauts et de suggérer des causes racines probables.

#### 🔹 Automatisation de tests auto-réparatrice  
Utiliser l'IA pour détecter les changements d'interface et d'API et adapter automatiquement les scripts de test afin de réduire les coûts de maintenance.

#### 🔹 Surveillance continue de la qualité (QA Ops)  
Appliquer l'IA pour surveiller les signaux de qualité dans les pipelines CI/CD, les environnements de production et les boucles de retour utilisateur.

#### 🔹 Analyse prédictive de la qualité et des risques  
Prévoir les risques de qualité, l'impact des régressions et la préparation à la mise en production sur la base des données historiques, des changements de code et de la complexité du système.

#### 🔹 Revue de code et portes de qualité pilotées par l'IA  
Enrichir l'analyse statique et les revues de code avec des insights alimentés par l'IA, centrés sur la qualité, la testabilité et la maintenabilité.  

#### 🔹 Documentation vivante et extraction de connaissances  
Générer et mettre à jour en continu la documentation technique et fonctionnelle directement à partir de bases de code et de comportements système en constante évolution.  

---

## 🇬🇧 English

### Project Overview

This project explores how **Artificial Intelligence (AI)** can enhance **Software Quality Assurance (SQA)** practices.

Here is the basic structure of the project
```
portfolio-SQAAILab          Laboratory Root
│
├ nn-AI-topic-name          AI topic Root
│   │
│   ├ context               Information provided to AI to generate the result
│   ├ result
│   │   ├ doc               AI-generated documentation regarding the result
│   │   ├ src               AI-generated code regarding the result
│   │
│   ├ nn-README.md          General information about this topic of exploration
│   │
│
├ README.md                 General information about this portfolio-SQAAILab project
│
```

Each subfolder focuses on a specific AI-driven approach.  
Please refer to each **nn-README.md** file for detailed explanations, examples, and workflows.

🚀 **Vision:**   
The topics listed below represent the current areas of exploration. This repository is designed as a living laboratory for AI in Software Quality Assurance and will continuously evolve to experiment with, validate, and document emerging AI-driven techniques, tools, and paradigms as the field matures.

### Topics Covered

#### 🔹 Vibe Coding
10-AI-vibe-coding

An AI-driven development approach where developers use natural language prompts to guide Generative AI models (such as LLMs) to generate, refine, and debug code.

#### 🔹 Reverse Documentation
15-AI-doc-generation

An analytical approach that leverages existing source code to recreate missing, outdated, or undocumented specifications.

#### 🔹 Generative BDD
20-AI-QA-analysis-assistant

An AI-assisted approach to **Behavior-Driven Development (BDD)** that automates the generation of BDD scenarios, step definitions, and test scripts. Natural language requirements are transformed into structured **Gherkin (Given–When–Then)** syntax, helping to improve test coverage, reduce manual effort, and increase consistency across the software development lifecycle.

#### 🔹 AI-Generated Test Design  
20-AI-QA-analysis-assistant

Automatically deriving test cases, edge cases, and exploratory testing ideas from source code, user stories, APIs, and system behavior.

#### 🔹 Vibe Coding Tests  
25-AI-vibe-coding-tests

This is the major trend right now. Instead of worrying about strict code syntax, the tester focuses on the intent (the "vibe") and lets AI (like LLMs) generate the automation code. This makes it possible to create complex tests suites simply by describing the scenario in natural language.

#### 🔹 LLM RAG
30-AI-LLM-RAG  

"Large Language Model" with "Retrieval-Augmented Generation" - Consulting an authoritative knowledge base external to the AI ​​training data before generating a response using specific or sensitive information such as local documents, databases, web pages, personal notes, etc.

---
### 🔮 Future Areas of Exploration

As this project evolves, it aims to explore a broader range of AI-driven capabilities across the Software Quality Assurance lifecycle, including (but not limited to):

#### 🔹 Autonomous / Agentic Testing
Agents that autonomously plan, execute, diagnose, and adapt test suites (including self-healing) across the QA lifecycle with minimal human intervention (A part is already covered under "Vibe Coding Tests").

#### 🔹 Model Context Protocol (MCP) for QA Tooling
Standardizing how AI agents connect to test tools, data sources, environments, and CI/CD systems through a common protocol 

#### 🔹 Context Engineering
Deliberately designing, curating, and managing what an AI agent sees at each step — memory, retrieved documents, tool outputs, conversation history — to sustain performance as context grows. Goes beyond basic RAG toward agentic retrieval and multi-source context assembly for QA tasks.

#### 🔹 Multi-Agent QA Orchestration
Coordinating teams of specialized AI agents (e.g., one reviewing code changes, one generating test data, one executing and analyzing results) working in parallel across the SQA lifecycle, rather than relying on a single general-purpose agent.

#### 🔹 Intelligent Test Data Generation  
Creating realistic, compliant, and scenario-focused test data using Generative AI and synthetic data techniques.

#### 🔹 AI-Assisted Bug Detection & Root Cause Analysis  
Leveraging AI to analyze logs, traces, test results, and code changes to proactively identify defects and suggest probable root causes.

#### 🔹 Self-Healing Test Automation  
Using AI to detect UI and API changes and automatically adapt test scripts to reduce maintenance costs.

#### 🔹 Continuous Quality Monitoring (QA Ops)  
Applying AI to monitor quality signals in CI/CD pipelines, production environments, and user feedback loops.

#### 🔹 Predictive Quality & Risk Analysis  
Forecasting quality risks, regression impact, and release readiness based on historical data, code changes, and system complexity.

#### 🔹 AI-Driven Code Review & Quality Gates  
Enhancing static analysis and code reviews with AI-powered insights focused on quality, testability, and maintainability.  

#### 🔹 Living Documentation & Knowledge Extraction  
Continuously generating and updating technical and functional documentation directly from evolving codebases and system behavior.  
