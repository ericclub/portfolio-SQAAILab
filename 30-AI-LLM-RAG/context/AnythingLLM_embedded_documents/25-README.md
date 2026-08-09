*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

### 25-AI-vibe-coding-tests  
  
#### Assisté par IA  
  
Cette section du projet se concentre sur l'application de techniques d'IA au **vibe coding IA**.  
  
#### Objectifs  
  
Étant donné que notre logiciel n'a pas de suite de tests automatisés  
  
En tant qu'expert QA développeur de tests automatisés, en utilisant le fichier user_stories.md  
Je veux créer des tests d'intégration et unitaires automatisés, mais pas de tests de bout en bout ; nous nous en occuperons plus tard.  
et je veux qu'un test_guide.md au format markdown soit généré, expliquant comment exécuter les tests, où se trouvent les logs de résultats, etc.  
Ainsi nous aurons une première suite de tests automatisés couvrant le comportement actuel du logiciel, à utiliser et ajuster à l'avenir  
  
#### Outils & Technologies  
  
1. **Modèles d'IA :** Claude Opus 4.5 (mode pro activé)  
2. **Frameworks :** pytest  
  
#### Comment j'ai procédé  
  
1. J'ai utilisé comme contexte le document 'user_stories.md' (voir le sujet précédent « Analyse QA alimentée par l'IA »)  
2. J'ai aussi mis le code du logiciel en contexte pour démontrer cet usage de l'IA  
3. J'ai utilisé un prompt précis et solide au format RCTEFT (Role, Context, Tasks, Example, Format, Tone)  
   Voir 25-AI-vibe-coding-test/context/PROMPTS.md  
4. J'ai utilisé Claude Opus 4.5 (mode pro activé)  
  
ℹ️ Voir AI_Chat_History.md pour les détails  
  
#### Résultats  
  
Voici ce que l'IA a produit pour moi :  
  
* Elle a analysé mon projet pour identifier la technologie à utiliser. (Pytest)  
* Elle a installé Pytest et toutes les dépendances associées selon les exigences du projet.  
* **Elle a testé et ajusté son installation.**  
* Elle a créé la structure de la suite de tests comme demandé.  
* Elle a écrit tous les tests unitaires optimaux comme attendu.  
* Elle a écrit tous les tests d'intégration optimaux comme attendu.  
* Elle n'a pas immédiatement généré les tests e2e comme demandé (cela sera traité dans une section ultérieure de mon laboratoire).  
* Elle a exécuté la suite de tests.  
* **Elle a détecté des tests instables (flaky) dus à mon environnement extrêmement rapide.**  
* **Elle a corrigé les tests instables et expliqué la cause racine et les ajustements effectués.**  
* L'exécution des tests s'affiche dans la console comme demandé.  
* Elle a créé le script d'exécution des tests, qui permet plusieurs méthodes d'exécution.  
* Elle a généré un document. 'test_guide.md' est TRÈS complet, couvrant tout ce qu'il faut savoir sur la suite de tests et son utilisation.  
  
Elle a fait tout cela, imaginez :) , en 9 minutes !!!  
  
#### Mes découvertes IA  
  
Tous mes sujets IA couverts jusqu'à présent comportent deux points clés que j'ai appris :  
  
**1. Le prompting**  
C'est la clé qui permet à l'expert QA de diriger/utiliser l'IA de manière optimale pour générer le bon résultat du premier coup.  
  
**2. La vitesse de production TRÈS élevée de l'IA**  
C'est un super assistant qui produit des résultats des centaines de fois plus vite que si nous produisions l'équivalent manuellement.  
  
Maintenant, il est très important que l'humain reste responsable de ce qui a été produit par un agent IA.  
  
Donc, dans ce travail, j'ai revu/confirmé tout ce qui a été produit en comparant le contexte de données à la sortie, et j'ai confirmé que tout était optimal !  
  
Pour vous donner une idée de la valeur ajoutée de l'IA dans ce projet,  
  
si je regarde tout ce que l'IA a produit pour moi (voir la section résultats),  
  
j'estime que le travail manuel sans IA aurait pris entre 3 et 5 jours pour obtenir des résultats similaires.  
  
Voici le temps que cela m'a pris avec l'assistance de l'IA :  
  
* Écrire manuellement un bon prompt (RCTEFT) au départ pour définir et communiquer clairement mes attentes à l'IA  
  Environ 1 heure  
* Sortie générée par l'IA  
  Environ 9 minutes !  
* Révision manuelle de ce qui a été produit par rapport au contexte fourni et demandé. Révision confirmée dès la première  
  Environ 2 heures  
  
**Ma conclusion,**  
  
* Manuellement = 3 à 5 jours  
* Assisté par IA & Révisé manuellement = 3 heures.  
  
Je crois vraiment que nous ne pourrons plus nous passer de l'IA (de manière positive) pour les tests logiciels.  
L'IA aidera grandement l'industrie à livrer des logiciels de haute qualité beaucoup plus rapidement et facilement.  
  
N'hésitez pas à partager vos commentaires.  
Eric.  

---

## 🇬🇧 English

### 25-AI-vibe-coding-tests  
  
#### AI-Assisted  
  
This section of the project focuses on applying AI techniques to **AI vibe coding**.  
  
#### Objectives  
  
Because our software does not have an automated test suite  
  
As a QA expert automated test developer, using the user_stories.md file  
I want to create automated integration and unit tests, but no end-to-end tests; we'll handle those later.  
and I want a markdown test_guide.md to be generated that will explain how to run the tests, where are the results log etc.  
So we will have a first automated tests suites covering the actual software behavior to be used and adjusted in the future  
  
#### Tools & Technologies  
  
1. **AI Models:** Claude opus 4.5 (pro mode activated)  
2. **Frameworks:** pytest  
  
#### How proceeded  
  
1. I used as context the 'user_stories.md' document (see previous topic "AI-powered QA Analysis")  
2. I put the software code also as context to be used to demonstrate this AI usage  
3. I used a strong precise prompt using the RCTEFT format (Role, Context, Tasks, Example, Format, Tone)  
   See 25-AI-vibe-coding-test/context/PROMPTS.md  
4. I used Claude Opus 4.5 (pro mode activated)  
  
ℹ️ See AI_Chat_History.md for details  
  
#### Results  
  
Here's what the AI ​​produced for me:  
  
* It analyzed my project to identify the technology to use.  (Pytest)  
* It installed Pytest and all associated requirements according to the project requirements.  
* **It tested and adjusted its installation.**  
* It created the test suite structure as requested.  
* It wrote all the optimal unit tests as expected.  
* It wrote all the optimal integration tests as expected.  
* It did not immediately generate the e2e tests as requested (this will be addressed in a later section of my lab).  
* It ran the test suite.  
* **It detected flaky tests due to my extremely fast environment.**  
* **It corrected the flaky tests and explained the root cause and adjustments it made.**  
* The test execution is displayed in the console as requested.  
* It created the test execution script, which allows for multiple execution methods.  
* It generated a document. 'test_guide.md' is VERY comprehensive, covering everything you need to know about the test suite and its use.  
  
He did all that, get this :) , in 9 minutes!!!  
  
#### My AI Discoveries  
  
All my AI topics covered so far have two key points that I've learned:  
  
**1. Prompting**  
This is the key that allows the QA expert to dictate/use the AI ​​optimally to generate the right result the first time.  
  
**2. The AI's VERY high production speed**  
It's a super assistant that produces results hundreds of times faster than if we produced the equivalent manually.  
  
Now, it's very important that the human remains responsible for what has been produced by an AI Agent.  
  
So, in this work, I reviewed/confirmed everything that was produced by comparing the data context to the output, and I confirmed that everything was optimal!  
  
To give you an idea of ​​the added value of AI in this project,  
  
if I look at everything the AI ​​produced for me (see the results section),  
  
I estimate that manual work without AI would have taken between 3 and 5 days to achieve similar results.  
  
Here's the time it took me with AI assistance:  
  
* Manually write a good prompt (RCTEFT) at the beginning to clearly define and communicate my expectations to the AI  
  Approx. 1 hour  
* AI-generated output  
  Approx 9 minutes!  
* Manual review of what was produced versus the provided and requested context. Review confirmed on the first  
  Approx. 2 hours  
  
**My conclusion,**  
  
* Manually = 3 to 5 days  
* AI assisted & Manually Reviewed = 3 hours.  
  
I truly believe that we will no longer be able to do without AI (in a positive way) for software testing.  
AI will greatly help the industry to deliver high-quality software much faster and more easily.  
  
Please feel free to share your comments.  
Eric.  
