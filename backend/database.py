import sqlite3

class Database:
    """
    Janky wrapper around SQLite because I don't want to fogure out SQLAlchemy or threading
    """
    def __init__(self, path: str) -> None:
        self.path = path

    def setup(self):
        database_connection = sqlite3.connect(self.path)
        cursor = database_connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            prompt TEXT,
            brand_name TEXT,
            brand_score REAL,
            augmented_prompt TEXT,
            model_backend TEXT,
            image_path TEXT,
            openai_response TEXT
        )
        """)

        database_connection.commit()
        database_connection.close()


    def log_image(self, prompt: str, company_name: str, company_score: float, augmented_prompt: str, model_backend: str, image_path: str, openai_response: str):
        local_connection = sqlite3.connect(self.path)
        cursor = local_connection.cursor()

        cursor.execute("""
        INSERT INTO images (prompt, brand_name, brand_score, augmented_prompt, model_backend, image_path, openai_response)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (prompt, company_name, company_score, augmented_prompt, model_backend, image_path, openai_response))

        local_connection.commit()
        local_connection.close()

    def get_all_images(self):
        local_connection = sqlite3.connect(self.path)
        cursor = local_connection.cursor()

        cursor.execute("SELECT * FROM images")
        rows = cursor.fetchall()

        local_connection.close()

        return rows