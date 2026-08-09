*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

___
**IA :**      
**Fichiers de contexte :**      
**Prompt de démarrage :**       

------ Meilleur prompt générique RCTFET 

[Rôle]
...
[Contexte]
...
[Tâches]
...
[Format]
...
[Exemple]
...
[Ton]
...


------ Meilleur prompt Mistral 

[Contexte]         (Poser le décor)

Vous êtes :             (Vous êtes un expert en marketing digital.)
L'objectif :            (M'aider à concevoir une stratégie de réseaux sociaux pour une startup.)
Audience :              (Public cible : les milléniaux intéressés par le développement durable.)

[Tâche]            (Être précis)

Je veux :              (Générer 3 idées de publications avec légendes et hashtags.)
Format :              (Les lister dans un tableau avec des colonnes pour la plateforme, la légende et les hashtags.)

[Contraintes]     (Fixer des limites)

Ton :                (Amical, professionnel et motivant.)
Longueur :              (Les légendes doivent faire moins de 150 caractères.)
À éviter :               (Pas de jargon ni d'argot.)

[Exemples]        (Si utile)

Bons/mauvais exemples :   (Voici une publication que j'ai aimée..)

[Résultat]          (Clarifier la livraison)

Doit ressembler à :    (Retourner sous forme de tableau markdown.)
Éléments supplémentaires :          (Inclure une brève justification pour chaque idée.)

------ Meilleur prompt ChatGPT 

Tu es un(e) [RÔLE].

Ta tâche est de [OBJECTIF].

Contexte :
- Contexte général :
- Contraintes :
- Audience :

Entrée :
[DONNÉES ou "aucune"]

Format de sortie :
- Structure :
- Longueur :
- Langue :

Exigences :
- Niveau de précision :
- Style :
- Ton :

Optionnel :
- Exemple :
- Étapes de validation avant la réponse finale


------ Meilleur prompt Gemini 

<system_instruction>
  Tu es un(e) expert(e) en [Rôle/Persona]. Ton objectif est de [Objectif principal].
  Suis strictement la logique définie dans la section <workflow>.
</system_instruction>

<context>
  <background>
    [Fournir ici le contexte général ou l'historique]
  </background>
  <constraints>
    [Lister ce que l'IA NE DOIT PAS faire ou les limitations spécifiques]
  </constraints>
</context>

<task_details>
  <workflow>
    1. D'abord, analyse les <source_data>.
    2. Ensuite, utilise les <examples> fournis pour comprendre le ton.
    3. Enfin, produis le résultat dans les balises <final_response>.
  </workflow>
  
  <source_data>
    [Coller ici vos données brutes, article ou code]
  </source_data>

  <examples>
    <example_1>
      <input>[Exemple d'entrée]</input>
      <output>[Résultat attendu]</output>
    </example_1>
  </examples>
</task_details>

<output_format>
  <style>[ex. Professionnel, Académique, Concis]</style>
  <structure>
    Utilise les balises XML suivantes dans ta réponse :
    <thinking> pour ton raisonnement interne.
    <final_response> pour la réponse finale.
  </structure>
</output_format>

------ Meilleur prompt Claude 

[RÔLE]
Tu es [rôle/expertise spécifique].

[CONTEXTE]
[Informations de contexte pertinentes, contraintes ou situation]

[TÂCHE]
[Description claire et précise de ce que tu veux]

[FORMAT]
[Format de sortie souhaité, longueur, style]

[EXEMPLES] (optionnel mais puissant)
Entrée : [exemple d'entrée]
Sortie : [exemple de sortie]

[CONTRAINTES] (si nécessaire)
- [Limitation spécifique 1]
- [Limitation spécifique 2]

------ Meilleur prompt Copilot 

Tu es [RÔLE/PERSONA].

Ta tâche : [OBJECTIF CLAIR].

Contexte :
[INFORMATIONS DE CONTEXTE]

Exigences de sortie :
- [FORMAT]
- [TON]
- [LONGUEUR]
- [STRUCTURE]

Exemples (optionnel) :
[EXEMPLES DE STYLE OU DE QUALITÉ]

Contraintes :
- [RÈGLES OU LIMITES]

Instruction finale :
Fournis la réponse finale dans un format soigné et prêt à l'emploi.

------ Meilleur prompt Grok 

Tu es [DESCRIPTION DU RÔLE/PERSONA]. Tu es un(e) expert(e) en [DOMAINE/COMPÉTENCES PERTINENTES], reconnu(e) pour être [TRAITS CLÉS, ex. rigoureux, créatif, concis, impartial].

Objectif/Tâche : [ÉNONCER CLAIREMENT L'OBJECTIF OU LA QUESTION PRINCIPALE].

Contexte/Historique : [FOURNIR ICI TOUTE INFORMATION, DÉTAIL, CONTRAINTE OU DONNÉE PERTINENTE. Soyez précis pour éviter toute ambiguïté.]

Consignes :
- Réfléchis étape par étape avant de répondre.
- Utilise un raisonnement logique et explique ton cheminement de pensée si pertinent.
- [TOUTE RÈGLE SUPPLÉMENTAIRE, ex. Reste factuel ; Évite les biais ; Limite la réponse à 500 mots ; Sois encourageant].

[OPTIONNEL : Exemples few-shot]
Exemple 1 :
Entrée : [EXEMPLE D'ENTRÉE]
Sortie : [SORTIE ATTENDUE AVEC RAISONNEMENT]

Exemple 2 :
...

Format de sortie :
[SPÉCIFIER LA STRUCTURE EXACTE, ex. :
- Utiliser des puces ou une liste numérotée
- Commencer par un résumé
- Terminer par les points clés à retenir
- Répondre en JSON : {"section1": "...", "section2": "..."}
- Utiliser le markdown pour les titres/tableaux]

Maintenant, réponds à ceci : [VOTRE VÉRITABLE REQUÊTE OU ENTRÉE ICI].

---

## 🇬🇧 English

___
**AI :**      
**Context files :**      
**Starting Prompt :**       

------ RCTFET Generic best prompt 

[Role]
...
[Context]
...
[Tasks]
...
[Format]
...
[Example]
...
[Tone]
...


------ Mistral best prompt 

[Context]         (Set the Stage)

You are:             (You are an expert in digital marketing.)
The goal:            (Help me craft a social media strategy for a startup.)
Audience:            (Target audience: millennials interested in sustainability.)

[Task]            (Be Specific)

I want:              (Generate 3 post ideas with captions and hashtags.)
Format:              (List them in a table with columns for platform, caption, and hashtags.)

[Constraints]     (Set Boundaries)

Tone:                (Friendly, professional, and motivational.)
Length:              (Captions should be under 150 characters.)
Avoid:               (No jargon or slang.)

[Examples]        (If Helpful)

Good/bad examples:   (Here's a post I liked..)

[Output]          (Clarify Delivery)

Should look like:    (Return as a markdown table.)
Any extras:          (Include a brief rationale for each idea.)

------ ChatGPT best prompt 

You are a [ROLE].

Your task is to [GOAL].

Context:
- Background:
- Constraints:
- Audience:

Input:
[DATA or "none"]

Output format:
- Structure:
- Length:
- Language:

Requirements:
- Accuracy level:
- Style:
- Tone:

Optional:
- Example:
- Validation steps before final answer


------ Gemini best prompt 

<system_instruction>
  You are an expert [Role/Persona]. Your goal is to [Main Objective].
  Follow the logic defined in the <workflow> section strictly.
</system_instruction>

<context>
  <background>
    [Provide high-level context or history here]
  </background>
  <constraints>
    [List what the AI MUST NOT do or specific limitations]
  </constraints>
</context>

<task_details>
  <workflow>
    1. First, analyze the <source_data>.
    2. Then, use the <examples> provided to understand the tone.
    3. Finally, produce the output inside <final_response> tags.
  </workflow>
  
  <source_data>
    [Paste your raw data, article, or code here]
  </source_data>

  <examples>
    <example_1>
      <input>[Sample Input]</input>
      <output>[Expected Output]</output>
    </example_1>
  </examples>
</task_details>

<output_format>
  <style>[e.g., Professional, Academic, Concise]</style>
  <structure>
    Use the following XML tags in your response:
    <thinking> for your internal reasoning.
    <final_response> for the actual answer.
  </structure>
</output_format>

------ Claude best prompt 

[ROLE]
You are [specific role/expertise].

[CONTEXT]
[Relevant background information, constraints, or situation]

[TASK]
[Clear, specific description of what you want]

[FORMAT]
[Desired output format, length, style]

[EXAMPLES] (optional but powerful)
Input: [example input]
Output: [example output]

[CONSTRAINTS] (if needed)
- [Specific limitation 1]
- [Specific limitation 2]

------ Copilot best prompt 

You are [ROLE/PERSONA].

Your task: [CLEAR GOAL].

Context:
[BACKGROUND INFORMATION]

Output Requirements:
- [FORMAT]
- [TONE]
- [LENGTH]
- [STRUCTURE]

Examples (optional):
[EXAMPLES OF STYLE OR QUALITY]

Constraints:
- [RULES OR LIMITS]

Final instruction:
Provide the final answer in a polished, ready-to-use format.

------ Grok best prompt 

You are [ROLE/PERSONA DESCRIPTION]. You are an expert in [RELEVANT FIELD/SKILLS], known for being [KEY TRAITS, e.g., thorough, creative, concise, unbiased].

Goal/Task: [CLEARLY STATE THE MAIN OBJECTIVE OR QUESTION].

Context/Background: [PROVIDE ANY RELEVANT INFORMATION, DETAILS, CONSTRAINTS, OR DATA HERE. Be specific to avoid ambiguity.]

Guidelines:
- Think step by step before responding.
- Use logical reasoning and explain your thought process where appropriate.
- [ANY ADDITIONAL RULES, e.g., Stay factual; Avoid bias; Keep response under 500 words; Be encouraging].

[OPTIONAL: Few-shot examples]
Example 1:
Input: [EXAMPLE INPUT]
Output: [DESIRED EXAMPLE OUTPUT WITH REASONING]

Example 2:
...

Output Format:
[SPECIFY EXACT STRUCTURE, e.g.:
- Use bullet points or numbered steps
- Start with a summary
- End with key takeaways
- Respond in JSON: {"section1": "...", "section2": "..."}
- Use markdown for headings/tables]

Now, respond to this: [YOUR ACTUAL QUERY OR INPUT HERE].
