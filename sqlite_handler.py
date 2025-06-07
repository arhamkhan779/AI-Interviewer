import sqlite3

class SqliteHandler:

    @staticmethod
    def find_all(dbname, collectionname):
        try:
            with sqlite3.connect(dbname) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {collectionname}")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return []

    @staticmethod
    def find_one_by_field(dbname, collectionname, field, value):
        try:
            with sqlite3.connect(dbname) as conn:
                cursor = conn.cursor()
                query = f"SELECT * FROM {collectionname} WHERE {field} = ?"
                cursor.execute(query, (value,))
                return cursor.fetchone() or []
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return []

    @staticmethod
    def find_many_by_field(dbname, collectionname, field, value):
        try:
            with sqlite3.connect(dbname) as conn:
                cursor = conn.cursor()
                query = f"SELECT * FROM {collectionname} WHERE {field} = ?"
                cursor.execute(query, (value,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return []

    @staticmethod
    def insert_row(dbname, collectionname, id, age, name):
        try:
            with sqlite3.connect(dbname) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO {collectionname} (id, age, name) VALUES (?, ?, ?)",
                    (id, age, name)
                )
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return False

    @staticmethod
    def update_row(dbname, collectionname, target_field, new_value, condition_field, condition_value):
        try:
            with sqlite3.connect(dbname) as conn:
                cursor = conn.cursor()
                query = f"""
                    UPDATE {collectionname}
                    SET {target_field} = ?
                    WHERE {condition_field} = ?
                """
                cursor.execute(query, (new_value, condition_value))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return False

    @staticmethod
    def delete_row(dbname, collectionname, condition_field, condition_value):
        try:
            with sqlite3.connect(dbname) as conn:
                cursor = conn.cursor()
                query = f"DELETE FROM {collectionname} WHERE {condition_field} = ?"
                cursor.execute(query, (condition_value,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return False

    @staticmethod
    def create_collection(dbname, collection_name, *columns):
        try:
            with sqlite3.connect(dbname) as conn:
                cursor = conn.cursor()
                column_definitions = ', '.join(columns)
                sql_query = f'''
                CREATE TABLE IF NOT EXISTS {collection_name} (
                    {column_definitions}
                )
                '''
                cursor.execute(sql_query)
                conn.commit()
                print(f"Collection (table) '{collection_name}' created successfully in '{dbname}'.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
