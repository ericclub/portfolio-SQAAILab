## 25-AI-vibe-coding-tests  
  
### AI-Assisted  
  
This section of the project focuses on applying AI techniques to **AI vibe coding**.  
  
### Objectives  
  
Because our software does not have an automated test suite  
  
As a QA expert automated test developer, using the user_stories.md file  
I want to create automated integration and unit tests, but no end-to-end tests; we'll handle those later.  
and I want a markdown test_guide.md to be generated that will explain how to run the tests, where are the results log etc.  
So we will have a first automated tests suites covering the actual software behavior to be used and adjusted in the future  
  
### Tools & Technologies  
  
1. **AI Models:** Claude opus 4.5 (pro mode activated)  
2. **Frameworks:** pytest  
  
### How proceeded  
  
1. I used as context the 'user_stories.md' document (see previous topic "AI-powered QA Analysis")  
2. I put the software code also as context to be used to demonstrate this AI usage  
3. I used a strong precise prompt using the RCTEFT format (Role, Context, Tasks, Example, Format, Tone)  
   See 25-AI-vibe-coding-test/context/PROMPTS.md  
4. I used Claude Opus 4.5 (pro mode activated)  
  
ℹ️ See AI_Chat_History.md for details  
  
### Results  
  
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
  
### My AI Discoveries  
  
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
* AI-assisted = 3 hours.  
  
I truly believe that we will no longer be able to do without AI (in a positive way) for software testing.  
AI will greatly help the industry to deliver high-quality software much faster and more easily.  
  
Please feel free to share your comments.  
Eric.  