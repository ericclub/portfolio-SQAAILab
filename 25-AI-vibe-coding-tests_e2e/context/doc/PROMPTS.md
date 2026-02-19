# DEMO
___
**AI :** VSCode AI Chat - Claude Opus 4.5  
**Context files :** None  
**Prompt :**  
```
I am a senior QA engineer (QA Ops, formerly a software developer).                      
The project I am currently working on involves optimizing AI-driven test automation.    
																						  
I would like:                                                                           
. A ready-to-use web application project, backend and frontend, executable on my PC In the 
. In DEMO-Vibe-Coding/result/src/app/backend subfolder, Its backend source code
. In DEMO-Vibe-Coding/result/src/app/frontend subfolder, Its frontend source code
. In DEMO-Vibe-Coding/result/doc subfolder, Its installation instructions guide 
. Be able to run it on my PC from VS Code                                               

The web application should be a simple web blog using, for example:                             
HTML, JavaScript, CSS, REST, Python, and a MySQL 

It would be beneficial to create a web page that allows users to:                       
. Create a user                                                                         
. List all users                                                                        
. View user details                                                                     
. Delete a user                                                                         
. Create a post                                                                         
. List all posts                                                                        
. View post details                                                                     
. Edit a post                                                                           
. Delete a post                                                                         
. View general statistics
```

___
**AI :** VSCode AI Chat - Claude Opus 4.5  
**Context files :** result/src
**Prompt :**  

```
[role]
Tu est un Analyste QA et développeur de test expérimenté

[context]

A partir du code sources
Je désire

. Dans un premier temps, avoir un plan de test avec User Story, Critéres d'acceptation et cas de test

[task]

À partir du code DEMO/result/src qui contiens d'éjà une petite application Web de blog
. Crée moi un plan de test qui doit être enregister dans DEMO/result/doc/test_plan.md en format markdown et en Français
. Ce plan de test doit être écrit de facons à produire 3 suites de tests 'end to end' pour chacune de ces principales section du logiciel (Users, Posts, Statistics)
. Ce plan de test doit contenire les stories, les critères d'acceptation ainsi que les cas de test
```

___
**AI :** VSCode AI Chat - Claude Opus 4.5  
**Context files :** DEMO/result/doc/test_plan.md, DEMO/result/src/app/* 
**Prompt :**  

```
role]
Tu est un développeur QA expérimenté avec Selenium/Python 

[Context]
À partir du document DEMO/result/doc/test_plan.md et du code source DEMO/result/src/app, j'ai besoin que tu me crée des suites de tests Sélénium / Python qui seront exécutable, qui s'afficheront dans la console lors de leur execution et dont le résultat sera écrit dans un rapport 

[task] 

Premièreement 

. Installation de Selenium pour Python 
. Pour être en mesure d'exécuté des test selenium sur l'application web DEMO/result/src/app
. Avec un rapport d'installation nommé DEMO/result/doc/INSTALL_Selenium.mkd

Deuxièment 

. Pour chacun des 'Cas de Test' dans DEMO/result/doc/test_plan.md et à partir du code source DEMO/result/src/app
. Crée moi un tests selenium dans le répertoire nommé DEMO/result/src/test_selenium/
. Le nom des tests selenium doivent contenir ces information FEATURE_PRIORITY_ID 

  exemple;

  FEATURE  = Nom de la 'Suite de tests'          insctit dans test_pan.md   (ex. Users ou Posts ou Statistics) 
  PRIORITY = Nom de la 'Priorité' du cas de test insctit dans test_pan.md   (ex. Haute ou Moyenne ou Basse)
  ID       = Nom du 'ID'          du cas de test insctit dans test_pan.md   (ex. TC-001-01, TC-001-02 etc.)

  exemple : Users_Haute_TC-001-01 
  exemple : Posts_Moyenne_TC-005-02
  exemple : Statistics_Basse_TC-011-02

. je désire être en mesure d'éxécute la suite des tests au complete 
. je désire être en mesure d'éxécute un test pour un ID spécifique 
. je désire être en mesure d'éxécute une suite de test que pour un FEATURE specifique 
. je désire être en mesure d'éxécute une suite de test que pour un FEATURE/PRIORITY specifique  
. je désire voir l'exécution des test et leur résultat dans la cosole 
. je désire avoir le résultat de l'exécution des test dans un rapport nommé ex: FEATURE_[timestamp].md dans le répertoire DEMO/result/src/test_selenium/reports
. Je désire avoir un document qui décrit l'utilisation, l'exécution des test selenium nommé DEMO/result/doc/selenium_test_suite_usage.md 
```
