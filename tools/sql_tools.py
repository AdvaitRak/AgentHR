import sqlite3

DB_PATH = "db/hr_agent_demo.sqlite"


def query_db(sql: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        conn.close()

        if not result:
            return "No results found."


        formatted = [dict(zip(headers, row)) for row in result]
        return formatted

    except Exception as e:
        return f"[ERROR in query]: {e}"


def update_db(sql: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return "✅ Update successful."
    except Exception as e:
        return f"[ERROR in update]: {e}"