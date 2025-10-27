import configparser
import psycopg2
from datetime import datetime

cfg = configparser.ConfigParser()
cfg.read('config.ini')

DB = cfg['database']
DB_DSN = f"host={DB['host']} port={DB['port']} dbname={DB['name']} user={DB['user']} password={DB['password']}"

def log_event(msg):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")

def get_client_record(client_id):
    log_event(f"Connecting to DB at {DB['host']} to fetch client {client_id}")
    conn = psycopg2.connect(DB_DSN, connect_timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT id, name, kyc_status FROM clients WHERE id = %s", (client_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def generate_greenbill_statement(client_id):
    # Business logic referencing Green Bill Bank (client-facing string in repo)
    client = get_client_record(client_id)
    if not client:
        return {"error": "client not found"}
    # Fake statement generation for "Green Bill Bank"
    statement = {
        "client_id": client[0],
        "client_name": client[1],
        "bank": "Green Bill Bank",
        "generated_at": datetime.utcnow().isoformat(),
        "status": client[2] or "pending"
    }
    return statement

if __name__ == "__main__":
    # quick local test (this shouldn't be used in prod; it's intentionally insecure)
    print(generate_greenbill_statement(42))
