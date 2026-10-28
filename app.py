from flask import Flask, request, redirect, render_template_string
import sqlite3
import os
app = Flask(__name__)
DB = "campusfix.db"

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        """)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CampusFix</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #eef4ff; margin: 0; padding: 24px; }
        main { max-width: 750px; margin: auto; }
        h1 { color: #1746a2; }
        form, .issue { background: white; padding: 18px; margin: 16px 0;
                       border-radius: 12px; }
        input, textarea, select, button {
            box-sizing: border-box; width: 100%; padding: 12px;
            margin: 7px 0; border: 1px solid #ccd5e5; border-radius: 7px;
        }
        button { background: #1746a2; color: white; cursor: pointer; }
        .status { color: #a15c00; font-weight: bold; }
    </style>
</head>
<body>
<main>
    <h1>CampusFix 🎓</h1>
    <p>Report campus problems and help make our college better.</p>

    <form method="POST" action="/report">
        <h2>Report an Issue</h2>
        <input name="title" placeholder="Issue title" required>
        <select name="category" required>
            <option value="">Select category</option>
            <option>Electrical</option>
            <option>Water</option>
            <option>Cleanliness</option>
            <option>Classroom</option>
            <option>Internet</option>
            <option>Other</option>
        </select>
        <input name="location" placeholder="Location in campus" required>
        <textarea name="description" placeholder="Describe the problem" required></textarea>
        <button type="submit">Submit Report</button>
    </form>

    <h2>Reported Issues</h2>
    {% for issue in issues %}
    <section class="issue">
        <h3>{{ issue[1] }}</h3>
        <p><b>Category:</b> {{ issue[2] }}</p>
        <p><b>Location:</b> {{ issue[3] }}</p>
        <p>{{ issue[4] }}</p>
        <p class="status">Status: {{ issue[5] }}</p>
    </section>
    {% else %}
    <p>No issues reported yet. You can submit the first report!</p>
    {% endfor %}
</main>
</body>
</html>
"""

@app.get("/")
def home():
    with sqlite3.connect(DB) as con:
        issues = con.execute(
            "SELECT id, title, category, location, description, status "
            "FROM issues ORDER BY id DESC"
        ).fetchall()
    return render_template_string(HTML, issues=issues)

@app.post("/report")
def report():
    fields = [
        request.form.get("title", "").strip(),
        request.form.get("category", "").strip(),
        request.form.get("location", "").strip(),
        request.form.get("description", "").strip()
    ]
    if all(fields):
        with sqlite3.connect(DB) as con:
            con.execute(
                "INSERT INTO issues (title, category, location, description) "
                "VALUES (?, ?, ?, ?)", fields
            )
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)),debug=False)