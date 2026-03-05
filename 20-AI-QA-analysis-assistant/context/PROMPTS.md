## 20-AI-stories-generation

___
**AI :** VSCode GPT 5.2  
**Context files :** app.py, index.html  
**Prompt :**  
```
[Context]

You are: 
An analyst helping to produce User Stories of the software   

The goal is: 
According theses given files of the actual software code;  
10-AI-vibe-coding\result\src\app\backend\app.py  
10-AI-vibe-coding\result\src\app\frontend\index.html  
I need you to produce user_stories.md file

Audience: 
Product Owner, QA, Developer 

[Task]

I want: 
According the given files (Backend Python file and Front End HTML file), analyse the code and produce a user_stories.md file that will described the fonctionnalities, their acceptance criteria and their test cases 

Format:
Markdown document
Have a table of contain at the beginning
Each functionalities will be described by CRUD User Stories, Acceptance Criteria and test cases.

User Stories format will follow: “As a [persona], I [want to], [so that].”
Acceptance criteria format of a story will follow: “Scenario: (explain scenario). Given (how things begin), when (action taken), then (outcome of taking action).”
```
___
**AI :** VSCode GPT 5.2  
**Context files :** user_stories,md, app.py, index.html  
**Prompt :**  
```
Based on the 'Test Pyramid Principle', in the user_stories.md file, are you able to identify (propose) 
which type of test to use (Unit test, Integration test, e2e test)
```
___
**AI :** VSCode GPT 5.2  
**Context files :** user_stories,md, app.py, index.html  
**Prompt :**  
```
In the current user_stories.md file, there don't seem to be any stories representing e2e type tests.
Could you add stories with Acceptance Criteria and Test Cases of the e2e type, while limiting the number of e2e type tests as recommended by the test pyramid principle?
```
