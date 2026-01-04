import json
from flask import Flask, request, render_template
import os
import hashlib

app = Flask(__name__)

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

    results = []

    if request.method == "POST":
        keyword = normalize(request.form.get("name", ""))
        print(f"Search query: {keyword}")

        if keyword:
            results = [
                s for s in data
                if keyword in normalize(s.get("Họ tên", ""))
            ]

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
