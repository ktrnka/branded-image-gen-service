from datetime import datetime
import json
import sqlite3
from typing import List, NamedTuple, Optional
import os.path

class GenerationResult(NamedTuple):
    created_at: int
    prompt: str
    brand_name: str
    brand_score: float
    augmented_prompt: str
    model_backend: str
    filename: Optional[str]
    debug_info: str

class EvaluationResult(NamedTuple):
    prompt: str
    brand_name: str
    augmented_prompt: str
    filename: str
    ref_brand_name: Optional[str]
    ref_augmented_prompt: Optional[str]
    ref_filename: Optional[str]

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

        # Evaluation table (same as V2)
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS evaluation_images (
            created_at INTEGER,
            prompt TEXT,
            brand_name TEXT,
            augmented_prompt TEXT,
            model_backend TEXT,
            code_version TEXT,
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
        debug_info: Optional[dict],
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
    FROM images_v2
    UNION
    SELECT
        created_at,
        prompt,
        brand_name,
        NULL AS brand_score,  -- This column doesn't exist in the 'evaluation_images' table, so we use NULL
        augmented_prompt,
        model_backend,
        filename as image_path,
        debug_info
    FROM evaluation_images;

                   """)
        rows = cursor.fetchall()

        local_connection.close()

        results = []
        for row in rows:
            created_at, prompt, brand_name, brand_score, augmented_prompt, model_backend, image_path, debug_info = row

            results.append(
                GenerationResult(
                    created_at=created_at,
                    prompt=prompt,
                    brand_name=brand_name,
                    brand_score=brand_score,
                    augmented_prompt=augmented_prompt,
                    model_backend=model_backend,
                    filename=os.path.basename(image_path) if image_path else None,
                    debug_info=debug_info,
                )
            )
        return results

    def has_evaluation(self, code_version: str, model_name: str) -> bool:
        local_connection = sqlite3.connect(self.path)
        cursor = local_connection.cursor()

        cursor.execute("select count(*) from evaluation_images where code_version = ? and model_backend = ?", (code_version, model_name))

        count = cursor.fetchone()[0]
        local_connection.close()

        return count > 0

    def get_evaluation(self, model_name: str, code_version: str, reference_code_version: str) -> List[GenerationResult]:
        local_connection = sqlite3.connect(self.path)
        cursor = local_connection.cursor()

        if reference_code_version:
            cursor.execute("""
select
    current.prompt,
    current.brand_name,
    current.augmented_prompt,
    current.filename,
    reference.brand_name as ref_brand_name,
    reference.augmented_prompt as ref_augmented_prompt,
    reference.filename as ref_filename
from evaluation_images current left join evaluation_images reference
on current.prompt = reference.prompt
where current.code_version = ? and current.model_backend = ? and reference.code_version = ? and reference.model_backend = ?
                       """, (code_version, model_name, reference_code_version, model_name))
        else:
            cursor.execute("""
select
    prompt,
    brand_name,
    augmented_prompt,
    filename,
    null as ref_brand_name,
    null as ref_augmented_prompt,
    null as ref_filename
from evaluation_images
where code_version = ? and model_backend = ?
                       """, (code_version, model_name))

        rows = cursor.fetchall()

        local_connection.close()
        
        return [EvaluationResult(*row) for row in rows]
    
    def log_evaluation_image(
        self,
        prompt: str,
        brand_name: str,
        augmented_prompt: str,
        model_backend: str,
        code_version: str,
        filename: str,
        debug_info: Optional[dict],
    ):
        debug_encoded = json.dumps(debug_info)

        local_connection = sqlite3.connect(self.path)
        cursor = local_connection.cursor()

        cursor.execute(
            """
        INSERT INTO evaluation_images (created_at, prompt, brand_name, augmented_prompt, model_backend, code_version, filename, debug_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                int(datetime.now().timestamp()),
                prompt,
                brand_name,
                augmented_prompt,
                model_backend,
                code_version,
                filename,
                debug_encoded,
            ),
        )

        local_connection.commit()
        local_connection.close()