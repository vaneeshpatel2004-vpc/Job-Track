from sqlalchemy import text
from app.database import engine

with engine.begin() as connection:

    columns = connection.execute(
        text("PRAGMA table_info(job_applications)")
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "user_id" not in column_names:

        connection.execute(
            text("""
                ALTER TABLE job_applications
                ADD COLUMN user_id INTEGER REFERENCES users(id)
            """)
        )

        connection.execute(
            text("""
                UPDATE job_applications
                SET user_id = 1
                WHERE user_id IS NULL
            """)
        )

        print("Migration completed successfully.")

    else:
        print("Migration already applied.")

    results = connection.execute(
        text("""
            SELECT id, company, job_title, user_id
            FROM job_applications
        """)
    ).fetchall()

    print("\nUpdated job applications:")

    for row in results:
        print(row)

    print("\nTotal applications:", len(results))