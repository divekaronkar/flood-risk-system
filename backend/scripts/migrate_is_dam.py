from app.db.session import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text('ALTER TABLE risk_locations ADD COLUMN is_dam TINYINT(1) NOT NULL DEFAULT 0'))
            conn.commit()
            print("Added is_dam column")
        except Exception as e:
            print(f"Error or already exists: {e}")

if __name__ == "__main__":
    migrate()
