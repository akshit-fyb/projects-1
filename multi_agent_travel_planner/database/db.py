import sqlite3, json
from pathlib import Path
DB=Path(__file__).resolve().parents[1]/'travel_planner.db'
def init_db():
    with sqlite3.connect(DB) as c: c.execute('CREATE TABLE IF NOT EXISTS trips(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, origin TEXT, destination TEXT, payload TEXT)')
def save_trip(origin,destination,payload):
    init_db()
    with sqlite3.connect(DB) as c: c.execute('INSERT INTO trips(origin,destination,payload) VALUES(?,?,?)',(origin,destination,json.dumps(payload,default=str)))
def recent_trips(limit=10):
    init_db()
    with sqlite3.connect(DB) as c: return c.execute('SELECT created_at,origin,destination FROM trips ORDER BY id DESC LIMIT ?',(limit,)).fetchall()
