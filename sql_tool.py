import sqlite3


class SQLTool:

    def get_employees(self):

        conn = sqlite3.connect(
            "data/databases/employees.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM employees"
        )

        rows = cursor.fetchall()

        conn.close()

        return rows