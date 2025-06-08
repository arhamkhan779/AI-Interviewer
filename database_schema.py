import sqlite3

def create_database_schema(db_name='interview_app.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 1. User_collection
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User_collection (
            user_Id INTEGER PRIMARY KEY,
            Name TEXT,
            Email TEXT
        )
    ''')

    # 2. QuestionBank_collection with new fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuestionBank_collection (
            user_Id INTEGER,
            programminglanguage TEXT,
            Level TEXT,
            GeneratedTimestamp TEXT,
            TotalQuestions INTEGER,
            Questions TEXT,
            FOREIGN KEY (user_Id) REFERENCES User_collection(user_Id)
        )
    ''')

    # 3. Q_A_Bank_collection with new field: TimeTaken
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Q_A_Bank_collection (
            user_Id INTEGER,
            question_number INTEGER,
            question TEXT,
            answer TEXT,
            TimeTaken TEXT,
            FOREIGN KEY (user_Id) REFERENCES User_collection(user_Id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database schema created successfully.")


