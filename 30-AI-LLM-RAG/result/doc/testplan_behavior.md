*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# Tests de performance (Max 10)

LLM local + RAG (LM Studio + AnythingLLM)

------------------------------------------------------------------------

# Table des matières

1.  Référence de performance (latence + tokens/sec)
2.  Concurrence / requêtes multiples
3.  Test de stress de la fenêtre de contexte
4.  Précision de récupération vs bruit (ajustement Top-K / seuil)
5.  Validation de mise à jour de document / réindexation
6.  Test d'ingestion de document volumineux
7.  Robustesse au non-texte / formatage (PDF, tableaux, blocs de code)
8.  Résistance à l'injection de prompt (basée sur document)
9.  Résilience réseau (déconnexion temporaire)
10. Test de régression lors du changement de modèle (qualité et compatibilité)
11. Astuce : suivre les résultats

------------------------------------------------------------------------

## 1) Référence de performance (latence + tokens/sec)

**Objectif :** Établir une référence pour la vitesse et la stabilité des réponses.

**Comment tester** 1. Dans AnythingLLM, poser le même prompt court 5 fois
(ex. « Respond only with OK. »). 2. Chronométrer chaque réponse. 3. Répéter avec un
prompt plus long.

**Attendu** - Le temps de réponse est cohérent. - Les prompts plus longs prennent plus de temps
mais restent stables.

**Critères de réussite** - Aucun timeout. - Les temps de réponse restent acceptables.

------------------------------------------------------------------------

## 2) Concurrence / requêtes multiples

**Objectif :** Vérifier le comportement du système sous des requêtes simultanées.

**Comment tester** 1. Ouvrir deux sessions de chat. 2. Envoyer des prompts en même
temps.

**Attendu** - Les requêtes sont mises en file d'attente correctement. - Aucun crash.

**Critères de réussite** - Les deux requêtes se terminent avec succès.

------------------------------------------------------------------------

## 3) Test de stress de la fenêtre de contexte

**Objectif :** S'assurer que le système gère des entrées de contexte volumineuses.

**Comment tester** 1. Coller un texte très long. 2. Demander une sortie structurée.

**Attendu** - Gestion élégante si le contexte est dépassé. - Aucune sortie
corrompue.

**Critères de réussite** - Aucun crash. - Sortie cohérente.

------------------------------------------------------------------------

## 4) Précision de récupération vs bruit (ajustement Top-K / seuil)

**Objectif :** Confirmer la récupération correcte des chunks.

**Comment tester** 1. Créer deux documents similaires avec des faits différents. 2. Poser
une question référençant ces faits. 3. Ajuster le Top-K et le seuil.

**Attendu** - La source correcte reste prépondérante. - Le seuil réduit le
bruit.

**Critères de réussite** - Réponse correcte cohérente.

------------------------------------------------------------------------

## 5) Validation de mise à jour de document / réindexation

**Objectif :** Vérifier que l'index se met à jour correctement.

**Comment tester** 1. Indexer un document avec une valeur connue. 2. Modifier la valeur. 3.
Réindexer et retester.

**Attendu** - La valeur mise à jour est retournée.

**Critères de réussite** - Aucune réponse obsolète.

------------------------------------------------------------------------

## 6) Test d'ingestion de document volumineux

**Objectif :** Valider l'indexation de fichiers volumineux.

**Comment tester** 1. Téléverser un PDF volumineux ou de nombreux fichiers. 2. Indexer. 3. Poser
plusieurs questions.

**Attendu** - Indexation réussie. - Récupération précise.

**Critères de réussite** - Aucun échec d'indexation.

------------------------------------------------------------------------

## 7) Robustesse au non-texte / formatage

**Objectif :** Valider la gestion des tableaux et des blocs de code.

**Comment tester** 1. Téléverser un PDF structuré ou un markdown avec du code. 2. Poser une
question spécifique sur un tableau/du code.

**Attendu** - Aucune ligne hallucinée. - Explication précise.

**Critères de réussite** - La sortie correspond au contenu source.

------------------------------------------------------------------------

## 8) Résistance à l'injection de prompt

**Objectif :** S'assurer que les instructions malveillantes présentes dans les documents sont ignorées.

**Comment tester** 1. Insérer une instruction malveillante dans un document. 2. Poser une
question neutre.

**Attendu** - Le modèle ignore l'instruction malveillante.

**Critères de réussite** - Comportement inchangé.

------------------------------------------------------------------------

## 9) Résilience réseau

**Objectif :** Valider la récupération après une interruption réseau.

**Comment tester** 1. Démarrer une génération. 2. Désactiver temporairement le réseau. 3.
Reconnecter et réessayer.

**Attendu** - Le système récupère. - Les requêtes suivantes réussissent.

**Critères de réussite** - Aucun échec permanent.

------------------------------------------------------------------------

## 10) Test de régression lors du changement de modèle

**Objectif :** Valider le changement de modèle en toute sécurité.

**Comment tester** 1. Changer de modèle instruct. 2. Tester le chat et le RAG. 3.
Revenir au modèle initial et retester.

**Attendu** - Aucune erreur « model not found ». - Le RAG reste fonctionnel.

**Critères de réussite** - Comportement stable lors des changements de modèle.

------------------------------------------------------------------------

## 11) Astuce : suivre les résultats

Enregistrer pour chaque test : - Date - Modèle utilisé - Paramètres - Réussite/Échec - Notes

---

## 🇬🇧 English

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
