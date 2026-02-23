import time,psycopg2,os
while True:
    try:
        psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        print("Database ready")
        break
    except Exception:
        print("Waiting for database...")
        time.sleep(1)