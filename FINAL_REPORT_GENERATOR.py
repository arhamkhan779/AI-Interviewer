import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlite_handler import SqliteHandler
load_dotenv()

sqlhandler = SqliteHandler()


class FinalReportGenerator:
    def __init__(self,user_id):
        self.user_id = user_id
        self.model = "gemini-2.0-flash"
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.user_collection = "User_collection"
        self.question_bank_collection = 'QuestionBank_collection'
        self.q_a_collection = 'Q_A_Bank_collection'
        self.database = 'interview_app.db'
    
    def setup_model(self) -> ChatGoogleGenerativeAI:
        model = ChatGoogleGenerativeAI(model = self.model , api_key=self.api_key)
        return model 
    
    def get_user_info(self) -> dict:
        results=sqlhandler.find_one_by_field(self.database,self.user_collection,field="user_id",value=self.user_id)
        print(results)
        return {
            "user_id":results[0],
            "name":results[1],
            "email":results[2]
        }

    def get_question_bank(self) -> dict:
        results=sqlhandler.find_one_by_field(self.database,self.question_bank_collection,field="user_id",value=self.user_id)
        
        return {
            "user_id":results[0],
            "programming_language":results[1],
            "level":results[2],
            "date":results[3],
            "total_questions":results[4]
        }


    def get_question_answer_bank(self) -> list:
        results = sqlhandler.find_many_by_field(self.database, self.q_a_collection, field="user_id", value=self.user_id)
        
        keys = ["user_id", "question_number", "question", "answer", "time_in_seconds"]
        
        dict_list = []
        for record in results:
            d = dict(zip(keys, record))
            d["time_in_seconds"] = float(d["time_in_seconds"])  # convert time to float
            dict_list.append(d)
        
        return dict_list

    def setup_prompt(self) -> str:
        user_info = self.get_user_info()
        q_a_list = self.get_question_answer_bank()
        interview_info = self.get_question_bank()

        total_time = sum(q['time_in_seconds'] for q in q_a_list)
        average_time = total_time / len(q_a_list) if q_a_list else 0

        qa_text = ""
        for q in q_a_list:
            qa_text += (
                f"Question {q['question_number']}:\n"
                f"{q['question']}\n\n"
                f"Answer:\n{q['answer']}\n"
                f"Time Taken: {q['time_in_seconds']:.2f} seconds\n\n"
            )

        prompt = f"""
    You are a creative AI and UI/UX expert. Your task is to generate a **DARK THEME** HTML report for a technical interview.

    ---

    ### 🎯 Objectives:
    - Dark mode UI with glowing modern components
    - Gradient headers and soft glow shadows
    - **Static** score circle with CSS-only styling (no JS animations)
    - Candidate info card, skill analysis, and recommendation
    - Fully responsive and visually engaging (PDF-compatible)
    - All content should be inside a single master container

    ---

    ### 🧑‍💻 Candidate:
    - Name: {user_info['name']}
    - ID: {user_info['user_id']}
    - Email: {user_info['email']}

    ### 📋 Interview Info:
    - Language: {interview_info["programming_language"]}
    - Level: {interview_info["level"]}
    - Date: {interview_info["date"]}
    - Questions: {interview_info["total_questions"]}
    - Time: {total_time:.2f} sec (avg: {average_time:.2f} sec)

    ---

    ### ✅ Report Sections (dark themed):

    1. **Header**
    - Title: "Technical Interview Evaluation Report"
    - Gradient background: `linear-gradient(90deg, #7F00FF, #E100FF)`
    - Font: `'Poppins'`, `'Inter'`, or `'Roboto'` via Google Fonts

    2. **Score Circle**
    - Display score out of 100
    - Use **static circular progress bar** using pure CSS (no animation)
    - Display score text in center

    3. **Candidate Info Card**
    - Dark gray-black background
    - Light text, glowing border
    - Include name, ID, email

    4. **Interview Summary Panel**
    - Total Questions, Time, Avg Time, Score
    - Style with glowing box and soft transitions (no JS-based animation)

    5. **Detailed Q&A Table**
    - Wrap inside a `<div class="table-container">` with `overflow-x: auto`
    - Use `<table style="table-layout: fixed; width: 100%">`
    - Columns: Q#, Question, Answer, Time Taken, Evaluation
    - Long answers:
        - Wrap inside `<div class="answer-box">`
        - Styles:
            - `max-height: 200px;`
            - `overflow-y: auto;`
            - `white-space: pre-wrap;`
            - `word-wrap: break-word;`
            - dark background, soft padding and glow
    - Evaluation tags: glowing badges:
        - ✅ Correct = Green
        - ❌ Incorrect = Red
        - ⚠️ Incomplete = Yellow

    6. **Skill Analysis**
    - Analyze answers and time taken
    - Present strengths and weaknesses with **CSS progress bars or star icons**
    - Style for dark UI (no JavaScript required)

    7. **Final Recommendation**
    - 2–3 line summary
    - Clearly state if the candidate is recommended or not

    8. **Dark Theme Styling**
    - Main background: `#111` or `#1e1e1e`
    - Font color: `#f0f0f0`, `#dcdcdc`
    - Gradients: `#00c6ff → #0072ff` or `#7F00FF → #E100FF`
    - Box shadows: `0 0 10px rgba(255, 255, 255, 0.1)`
    - Border radius: `12px`
    - **Do not use any JavaScript-based animation**
    - CSS/JS must be embedded internally (no external links except fonts)
    - Fully responsive (mobile to desktop)

    ---

    ### 🧾 Interview Q&A Raw Data:
    {qa_text}

    ---

    ### Your Task:
    - Evaluate each question and assign tag: Correct / Incorrect / Incomplete
    - Generate a score out of 100
    - Provide skill analysis (topics the student is strong/weak in)
    - Generate final recommendation
    - Produce a **single self-contained HTML report** in dark theme
    - Must include internal CSS and minimal JS for responsiveness only
    - Entire report should be wrapped in one master `<div class="report-container">`
    - Do **not** use Markdown or explanation — only return the full HTML
    """
        return prompt

    def get_html_report(self) -> str:
        model =self.setup_model()
        prompt = self.setup_prompt()
        response = model.invoke(prompt)
        return response.content[7:-3]
    
    def main(self) -> str:
        return self.get_html_report()

