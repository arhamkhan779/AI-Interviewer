from flask import Flask, render_template, jsonify, request, redirect, url_for,send_file
from sqlite_handler import SqliteHandler
from flask_cors import CORS
from QUESTION_GENERATION_MODULE import QuestionGeneration
from database_schema import create_database_schema
import os
import datetime
from TEXT_TO_SPEECH_MODULE import TextToSpeech
import re
from FINAL_REPORT_GENERATOR import FinalReportGenerator

db_name = 'interview_app.db'
user_collection = "User_collection"
question_bank_collection = 'QuestionBank_collection'
q_a_bank_collection = 'Q_A_Bank_collection'
final_report_collection = "Final_Report"


print(f"Creating Database Schema")
if os.path.exists(db_name):
    print("Database ALready Exists")
else:
    create_database_schema(db_name=db_name)


app = Flask(__name__)
CORS(app)

@app.route("/")
def index_template():
    return render_template("index.html")

@app.route("/home")
def home_template():
    return render_template("home.html")

@app.route("/past_interview")
def past_interview_template():
    return render_template("past_interview.html")

@app.route("/question_generation_template")
def question_generator_template():
    user_id = request.args.get("user_id")
    return render_template("question_generation.html",user_id=user_id)

@app.route("/interview_template")
def interview_template():
    user_id = request.args.get("user_id")
    return render_template("interview.html",user_id=user_id)

@app.route("/final_report_template")
def final_report_template():
    user_id = request.args.get("user_id")
    return render_template("final_report_template.html",user_id=user_id)

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        id = data["id"]
        action = data.get("action")

        if action == "register":
            user = SqliteHandler.find_one_by_field(db_name, 'User_collection', "user_id", id)
            if len(user) != 0:
                return jsonify({"response": "User Already Exist"})

            name = data["name"]
            email = data["email"]

            status, response = SqliteHandler.insert_row(
                db_name,
                user_collection,
                user_Id=id,
                Name=name,
                Email=email
            )
            return jsonify({"response": "User Registered Successfully"})

        elif action == "next":
            return jsonify({
                "redirect": url_for('question_generator_template', user_id=id)
            })

        else:
            return jsonify({"response": "Unknown action."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_question",methods=["POST"])
def generate_questions():
    try:
        user_id = request.args.get("user_id")
        existing_data = SqliteHandler.find_one_by_field(
            db_name, question_bank_collection, "user_Id", user_id
        )

        if existing_data:
            return jsonify({"response": "Question for that ID already generated. Proceed with Interview"})
        
        data = request.get_json()
        if not user_id or not data.get('language') or not data.get('level'):
             return jsonify({"response": "Missing required parameters."}), 400
        
        
        level = data['level']
        programming_language = data['language']
        obj = QuestionGeneration(programming_language,level)
        questions = obj.main() #It will return string
        total_questions = len(questions.split("//"))
        generated_timestamp = datetime.datetime.now().isoformat()

        status, response = SqliteHandler.insert_row(
            db_name,
            question_bank_collection,
            user_Id=user_id,
            programminglanguage=programming_language,
            Level=level,
            GeneratedTimestamp=generated_timestamp,
            TotalQuestions=total_questions,
            Questions=questions
        )
        if not status:
            return jsonify({"response": response})
        
        else:
           if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    "response": "Generated Successfully",
                    "redirect": url_for('interview_template', user_id=user_id)
                })
           else:
                return redirect(url_for('interview_template', user_id=user_id))

    except Exception as e:
        return jsonify({"repponse":e})


@app.route("/get_questions", methods=["GET"])
def get_user_questions():

    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    existing_data = SqliteHandler.find_one_by_field(
        db_name, question_bank_collection, "user_Id", user_id
    )

    if not existing_data:
        return jsonify({"response": "User does not exist"})
    else:
        data = {}
        id = existing_data[0]
        language = existing_data[1]
        level = existing_data[2]
        created_time = existing_data[3]
        total_quesitons = existing_data[4]
        questions = existing_data[5].split("//")
        question_number = 1
        for i in range(total_quesitons):
            data[question_number] = questions[i]
            question_number+=1
        return jsonify({"user_id":id,"questions":data,"level":level,"programming_language":language})


@app.route("/audio", methods=["POST"])
def audio():
    text = request.get_json()["text"]
    text = re.sub(r'[^A-Za-z0-9]', '', text)
    obj = TextToSpeech()
    audio_bytes = obj.convert_to_audio(text)
    
    return send_file(
        audio_bytes,
        mimetype="audio/mpeg",
        as_attachment=False,
        download_name="speech.mp3"
    )

@app.route("/save_answer", methods=["POST"])
def save_answer():
    data = request.get_json()
    
    user_id = request.args.get("user_id")
    question_number = data.get("question_number")
    question = data.get("question")
    answer = data.get("answer")
    time_taken = data.get("time_taken")

    if not all([user_id, question_number, question, answer]):
        return jsonify({"error": "Missing required fields"}), 400

    insert_data = {
        "user_Id": user_id,
        "question_number": question_number,
        "question": question,
        "answer": answer,
        "TimeTaken": time_taken
    }

    success, message = SqliteHandler.insert_row(
        dbname=db_name,
        collectionname="Q_A_Bank_collection",
        **insert_data
    )

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 500


@app.route("/generate_final_report",methods = ["POST"])
def generate_final_report():
    user_id = request.args.get("user_id")
    print(user_id)
    obj = FinalReportGenerator(user_id=user_id)
    report = obj.main()

    insert_data = {
        "user_id":user_id,
        "report": report
    }
    success, message = SqliteHandler.insert_row(
        dbname=db_name,
        collectionname=final_report_collection,
        **insert_data
    )
    return jsonify({"report":report})

@app.route("/get_final_report",methods = ["POST"])
def get_report():
    user_id = request.get_json()["user_id"]

    existing_data = SqliteHandler.find_one_by_field(
            db_name, final_report_collection, "user_Id", user_id
        )

    if len(existing_data) == 0:
            return jsonify({"response": "Data Does Not Exist with Id"})
    
    else:
        return jsonify({"report":existing_data[1]})
    
if __name__ == "__main__":
    app.run(debug=True)