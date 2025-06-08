import sqlite3

def list_tables(dbname):
    try:
        with sqlite3.connect(dbname) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return []

def describe_table(dbname, table_name):
    try:
        with sqlite3.connect(dbname) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            return columns
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return []

# Usage
db_name = "Main_Db.db"
tables = list_tables(db_name)
print("Tables in DB:", tables)

for table in tables:
    print(f"\nStructure of table '{table}':")
    description = describe_table(db_name, table)
    for col in description:
        cid, name, dtype, notnull, dflt_value, pk = col
        print(f" - {name} ({dtype}){' PRIMARY KEY' if pk else ''}")

# import sqlite3

# def clear_sqlite_tables(db_path):
#     try:
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()

#         # Get all table names except SQLite internal ones
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
#         tables = cursor.fetchall()

#         # Disable foreign keys temporarily
#         cursor.execute("PRAGMA foreign_keys = OFF;")

#         # Delete data from each table
#         for table_name in tables:
#             print(f"Clearing table: {table_name[0]}")
#             cursor.execute(f"DELETE FROM {table_name[0]};")

#         # Reset autoincrement counters
#         cursor.execute("DELETE FROM sqlite_sequence;")

#         conn.commit()
#         print("All tables cleared successfully.")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         conn.close()

# # Example usage
# clear_sqlite_tables("Main_Db.db")


from sqlite_handler import SqliteHandler
print(SqliteHandler.find_all("Main_Db.db",'QuestionBank_collection'))
# print(SqliteHandler.find_one_by_field("Main_Db.db",'User_collection',"user_id",90))

import sqlite3

DB_NAME = "Main_Db.db"
TABLES = ["User_collection", "QuestionBank_collection", "Q_A_Bank_collection"]

# def clear_all_tables():
#     try:
#         conn = sqlite3.connect(DB_NAME)
#         cursor = conn.cursor()
#         for table in TABLES:
#             cursor.execute(f"DELETE FROM {table}")
#             print(f"Cleared table: {table}")
#         conn.commit()
#         conn.close()
#         print("✅ All tables cleared successfully.")
#     except sqlite3.Error as e:
#         print(f"❌ Error clearing tables: {e}")

# if __name__ == "__main__":
#     clear_all_tables()
