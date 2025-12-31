import json
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
from models import SearchLog, db

app = Flask(__name__)

# Kết nối database (PostgreSQL trên Render)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def hash_ip(ip):
    if not ip:
        return None
    return hashlib.sha256(ip.encode()).hexdigest()

with open('KSK Le Loi 2025.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def normalize(text: str) -> str:
    return text.lower().strip()

@app.route('/', methods=['GET', 'POST'])
def home():
    query = request.form.get("name", "")

    if request.method == "POST" and query and len(query) >= 3:
        raw_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ip = raw_ip.split(",")[0].strip()

        ua = request.headers.get("User-Agent")

        log = SearchLog(
            query=query,
            ip_hash=hash_ip(ip),
            user_agent=ua
        )
        db.session.add(log)
        db.session.commit()
        
    results = []

    if request.method == "POST":
        keyword = normalize(request.form.get("name", ""))

        if keyword:
            results = [
                s for s in data
                if keyword in normalize(s.get("Họ tên", ""))
            ]

    return render_template('index.html', results=results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(port=5000, debug=True)
