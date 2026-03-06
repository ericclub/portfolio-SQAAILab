**AI :** VSCode ClaudeOpus4.5       
**Context files :**  
10-AI-vibe-coding\result  
20-AI-QA-analysis-assistant\result  

**Starting Prompt :**   

```
[Context]
 
You are:
You are an automated test developer
 
The goal:
Create the unit and integration tests recommended by the user_stories.md file
 
Audience:
Developer, QA Analyst

I want you to create automated integration and unit tests, but no end-to-end tests; we'll handle those later. 
I want to be able to run all tests or only unit tests or only integration tests

[Task]

Use as context                  10-AI-vibe-coding\result and 20-AI-QA-analysis-assistant\result
Unit test should be in          25-AI-vibe-coding-tests\result\test\unit folder
Integration test should be in   25-AI-vibe-coding-tests\result\test\integration folder
Tests should be executable on   10-AI-vibe-coding\result\src 
 
[Format]

You have complete freedom regarding the display format in the console.
The results log file must be in Markdown format.
 
[Tone]

Professional
 
[Output]

I want to see the executed tests and the results of each one in the console.
I also want the same information saved in a Markdown output file.
I want a markdown test_guide.md to be generated that will explain how to run the tests, where are the results log etc. 
```
