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

Good/bad examples:   (Here’s a post I liked..)

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


