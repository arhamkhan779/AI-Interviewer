# AI-Interviewer -> For Coding of Different Languages

Architecture and WorkFlows

##Step1
A Register Page for the Interview Initiation

-UserId -? Unique
-UserEmail
-Password



will save in UserCollection in Sqlite3
User Will Click on the Next Button -> trigger endpoint to insert row in user collection

##Step2
User will select Programming Language Here e.g Python , C++, C# and so on -> 10 Question
Click on Next
It will trigger an endpoint which will store all the question in another collection called as question bank

-UserId
-programming Language
-QuestionList

then User Click on Begin Interview
##Step3
It will trigger another endpoint which retireve the question bank of that user , and on the UI side 
it will ask each question one by one , also by writing also by voice , we will use gtts for text to speech , it wil give each question for 6 minute , and session will be of 60 minutes

once it get all the question and corresponding answers it will save that in another collection name as Question-Answer Bank with the UserId , if user miss any question , the answer for that will be empty and consider as not attempted

then user click on Finish Interview , and prompt to another page to generate the final report , we will get the question answer bank of that user will pass to LLm to generate the final report 

and then user can email that report to his email also 