import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate


class QuestionGeneration:
    '''
    python module to generate technical question
    based on the user selected programming
    language
    '''
    model = "gemini-2.0-flash"
    api_key = os.getenv("GEMINI_API_KEY")
    max_questions = 10

    def __init__(self,programming_language:str, level:str) -> str:
        self.programming_language = programming_language
        self.level = level

    @staticmethod
    def setup_model():
        model = ChatGoogleGenerativeAI(model = QuestionGeneration.model, api_key=QuestionGeneration.api_key)
        return model 
    
    def get_response(self,prompt,model):
        try:
            response = model.invoke(prompt)
            return response.content
        except Exception as e:
            return e

    def setup_prompt(self):
            formatted_prompt = '''
            You are an expert software engineering interviewer.

            Generate exactly {max_question} coding interview questions for the programming 
            language: **{programming_language}**.
            The difficulty level of these questions should be: **{level}**.

            Ensure the questions are diverse and cover a broad range of fundamental programming concepts including:

            - Conditional statements (if-else)
            - Loops (for, while)
            - Functions
            - Object-Oriented Programming (classes, inheritance, polymorphism)
            - Data Structures (arrays, lists, stacks, queues, trees, etc.)
            - Recursion
            - String manipulation
            - Error handling or exception management
            - Basic algorithmic logic (searching, sorting, etc.)

            **Format Requirement:**
            Return the questions as a single string, each question separated by a //.

            Do not number the questions, do not include explanations—just the raw questions.

            Ensure high quality, real-world technical questions.
            Generate Exact number of this question
            ###max_question = {max_question}
            '''
            return formatted_prompt.format(max_question = QuestionGeneration.max_questions,programming_language=self.programming_language,level= self.level)
    
    def main(self):
         prompt_formatted = self.setup_prompt()
         model = self.setup_model()
         response = self.get_response(prompt_formatted,model)
         return response
        
