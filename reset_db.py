from sqlalchemy import create_engine, text
from database import DATABASE_URL

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    # Drop all tables
    conn.execute(text("DROP TABLE IF EXISTS jobs CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))

    # Drop all custom enum types we created
    conn.execute(text("DROP TYPE IF EXISTS institute CASCADE;"))
    conn.execute(text("DROP TYPE IF EXISTS job_mode CASCADE;"))
    conn.execute(text("DROP TYPE IF EXISTS job_type CASCADE;"))

    conn.commit()
    print("Database completely reset!")
