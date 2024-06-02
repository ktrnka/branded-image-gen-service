from datetime import datetime
import json
import sqlite3
from typing import List, NamedTuple

class GenerationResult(NamedTuple):
    created_at: int
    prompt: str
    brand_name: str
    brand_score: float
    augmented_prompt: str
    model_backend: str
    image_path: str
    debug_info: str

class Database:
    """
    Janky wrapper around SQLite because I don't want to fogure out SQLAlchemy or threading
    """

    def __init__(self, path: str) -> None:
        self.path = path

    def setup(self):
        database_connection = sqlite3.connect(self.path)
        cursor = database_connection.cursor()

        # V1 table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS images (
            prompt TEXT,
            brand_name TEXT,
            brand_score REAL,
            augmented_prompt TEXT,
            model_backend TEXT,
            image_path TEXT,
            openai_response TEXT
        )
        """
        )

        # V2 table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS images_v2 (
            created_at INTEGER,
            prompt TEXT,
            brand_name TEXT,
            augmented_prompt TEXT,
            model_backend TEXT,
            filename TEXT,
            debug_info TEXT
        )
        """
        )

        database_connection.commit()
        database_connection.close()

    def log_image(
        self,
        original_prompt: str,
        brand_name: str,
        augmented_prompt: str,
        model_backend: str,
        filename: str,
        debug_info: dict,
    ):
        debug_encoded = json.dumps(debug_info)
        now = int(datetime.now().timestamp())

        local_connection = sqlite3.connect(self.path)
        cursor = local_connection.cursor()

        cursor.execute(
            """
        INSERT INTO images_v2 (created_at, prompt, brand_name, augmented_prompt, model_backend, filename, debug_info)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                now,
                original_prompt,
                brand_name,
                augmented_prompt,
                model_backend,
                filename,
                debug_encoded,
            ),
        )

        local_connection.commit()
        local_connection.close()

    def get_all_images(self) -> List[GenerationResult]:
        # TODO: Update this to union v1 and v2
        local_connection = sqlite3.connect(self.path)
        cursor = local_connection.cursor()

        cursor.execute("""
SELECT
    NULL AS created_at,  -- This column doesn't exist in the 'images' table, so we use NULL
    prompt,
    brand_name,
    brand_score,         -- This column doesn't exist in 'images_v2', so we'll include it here
    augmented_prompt,
    model_backend,
    image_path,
    openai_response AS debug_info  -- Rename openai_response to debug_info for consistency
FROM images
UNION
SELECT
    created_at,
    prompt,
    brand_name,
    NULL AS brand_score,  -- This column doesn't exist in the 'images_v2' table, so we use NULL
    augmented_prompt,
    model_backend,
    filename as image_path,
    debug_info
FROM images_v2;

                       """)
        rows = cursor.fetchall()

        local_connection.close()

        return [GenerationResult(*row) for row in rows]

