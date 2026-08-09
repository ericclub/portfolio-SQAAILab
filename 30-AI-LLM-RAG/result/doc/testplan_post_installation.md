*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# Tests post-installation

Validation et scénarios de test pour LLM local + RAG

------------------------------------------------------------------------

# Table des matières

1.  Objectif
2.  Cas de test : Aucun modèle téléchargé
3.  Cas de test : Modèle téléchargé et chargé
4.  Cas de test : La mémoire GPU est utilisée
5.  Cas de test : La réponse utilise uniquement les documents intégrés
6.  Cas de test : Réponse complète
7.  Cas de test : Réponse partielle
8.  Cas de test : Information non disponible dans les documents locaux
9.  Liste de contrôle de validation finale
10. Résultat

------------------------------------------------------------------------

# 1. Objectif

Ce document décrit comment tester et valider différents états du système
et comportements de réponse lors de l'utilisation de :

-   LM Studio (PC Gaming)
-   AnythingLLM (Portable)
-   RAG local avec documents intégrés

------------------------------------------------------------------------

# 2. Cas de test : Aucun modèle téléchargé

## Scénario

Aucun modèle LLM n'a été téléchargé ou chargé dans LM Studio.

## Comment tester

1.  Arrêter le serveur LM Studio.
2.  Décharger tout modèle actif.
3.  Démarrer le serveur local sans charger de modèle.
4.  Envoyer un prompt depuis AnythingLLM.

## Résultat attendu

-   L'API peut répondre mais la génération échoue.
-   Erreur telle que :
    -   "Model not found"
    -   "No model loaded"
    -   Réponse de complétion vide ou échouée.

## Critères de validation

Le système doit clairement indiquer que le modèle n'est pas chargé.

------------------------------------------------------------------------

# 3. Cas de test : Modèle téléchargé et chargé

## Scénario

Mistral 8B Instruct est téléchargé et chargé dans LM Studio.

## Comment tester

1.  Charger le modèle dans LM Studio.
2.  Confirmer qu'il apparaît via : curl.exe
    http://`<GamingPC_IP>`{=html}:1234/v1/models
3.  Depuis AnythingLLM, envoyer le prompt : "What do you know about SQAAILab?"

## Résultat attendu

Réponse : réponse mentionnant quelque chose à propos de SQAAILab qui n'est pas pertinent pour ce laboratoire. Voir Hallucination.png 

## Critères de validation

-   Le modèle génère une sortie cohérente en l'absence de document réellement intégré et sans prompt spécifique demandant d'utiliser uniquement le document intégré.
-   Aucune erreur API.
-   Temps de réponse cohérent avec l'inférence GPU.

------------------------------------------------------------------------

# 4. Cas de test : La mémoire GPU est utilisée

## Scénario

S'assurer que l'inférence utilise le GPU (RTX 3060) et non le CPU.

## Comment tester

Gestionnaire des tâches -> Performance -> GPU 
Envoyer un prompt depuis AnythingLLM

Attendu : - L'utilisation du calcul GPU augmente. - La mémoire GPU dédiée
augmente. Voir gpu.png

## Critères de validation

-   Consommation de mémoire GPU visible.
-   Inférence plus rapide qu'une exécution CPU uniquement.

------------------------------------------------------------------------

# 5. Cas de test : La réponse utilise uniquement les documents intégrés

## Scénario

S'assurer que les réponses RAG proviennent strictement des documents indexés.

## Comment tester
Dans AnythingLLM
1. Créer un espace de travail nommé "MyWorkspace"
2. Configurer un prompt système comme .. voir system_prompt.md 
2. Intégrer des documents .. ./context/doc/AnythingLLM_embedded_documents
3. Demander : "What do you know about SQAAILab? is the project code name?"

## Résultat attendu

La réponse fait référence à des informations contenues dans ./context/doc/AnythingLLM_embedded_documents qui sont pertinentes pour ce laboratoire.

Puis demander : "What color is the sky?"

## Résultat attendu

Le système doit répondre : "I cannot find this information in the provided
documents."

## Critères de validation

Aucune réponse hallucinée.

------------------------------------------------------------------------

# 6. Cas de test : Réponse complète

## Scénario

Le document contient une réponse détaillée complète.

## Comment tester

1.  Ajouter un document avec une explication à plusieurs points.
2.  Poser une question de synthèse large.

## Résultat attendu

La réponse inclut : - Tous les points clés - Une réponse structurée - Aucune
section manquante

## Critères de validation

La réponse couvre l'intégralité de la portée de la section du document.

------------------------------------------------------------------------

# 7. Cas de test : Réponse partielle

## Scénario

Le document ne contient qu'une partie de l'information demandée.

## Comment tester

1.  Ajouter un document contenant des données limitées.
2.  Poser une question plus large.

## Résultat attendu

La réponse inclut uniquement les données connues. Le système ne doit pas inventer de
détails manquants.

## Critères de validation

La réponse se limite à l'information disponible.

------------------------------------------------------------------------

# 8. Cas de test : Information non disponible dans les documents locaux

## Scénario

L'utilisateur pose une question en dehors des connaissances indexées.

## Comment tester

Demander : "What year was the company founded?" (si absent des documents)

## Résultat attendu

Le système doit répondre : - "The information is not available in the
provided documents." - Ou une réponse ancrée similaire.

## Critères de validation

-   Aucune hallucination
-   Déclaration de limitation claire
-   Aucun fait fabriqué

------------------------------------------------------------------------

# 9. Liste de contrôle de validation finale

✔ Modèle correctement chargé
✔ Mémoire GPU utilisée
✔ API accessible
✔ Embeddings fonctionnels
✔ RAG récupérant les bons chunks
✔ Aucune hallucination
✔ Gestion correcte des données manquantes

------------------------------------------------------------------------

# 10. Résultat

Si tous les tests réussissent, l'environnement LLM local + RAG est correctement
configuré et validé.

---

## 🇬🇧 English

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
