from flask import Flask, render_template, request, redirect, session, jsonify
from database import get_connection

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("register_login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cur = conn.cursor()

    existing = cur.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    if existing:
        conn.close()
        return render_template(
            "register_login.html",
            message="User email already registered"
        )

    cur.execute(
        "INSERT INTO users(name,email) VALUES (?,?)",
        (name,email)
    )

    conn.commit()
    conn.close()

    return render_template(
        "register_login.html",
        message="Registration successful"
    )
@app.route("/user_income")
def user_income():

    if "user_id" not in session:
        return jsonify([])

    conn = get_connection()
    cur = conn.cursor()

    data = cur.execute(
        "SELECT * FROM income WHERE user_id=? ORDER BY date DESC",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])

# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cur = conn.cursor()

    user = cur.execute(
        "SELECT * FROM users WHERE name=? AND email=?",
        (name,email)
    ).fetchone()

    conn.close()

    if user:

        session["user_id"] = user["user_id"]
        session["name"] = user["name"]

        return redirect("/dashboard")

    return render_template(
        "register_login.html",
        message="Invalid login details"
    )


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template("dashboard.html")


# ---------------- ADD EXPENSE ----------------

@app.route("/add_expense", methods=["POST"])
def add_expense():

    if "user_id" not in session:
        return redirect("/")

    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses(user_id,category,amount,date) VALUES (?,?,?,?)",
        (session["user_id"],category,amount,date)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- SHOW USER EXPENSES ----------------

@app.route("/user_expenses")
def user_expenses():

    conn = get_connection()
    cur = conn.cursor()

    data = cur.execute(
        "SELECT * FROM expenses WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])


@app.route("/total_expense")
def total_expense():

    conn = get_connection()
    cur = conn.cursor()

    result = cur.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return jsonify(dict(result))

@app.route("/categories")
def categories():

    conn = get_connection()
    cur = conn.cursor()

    data = cur.execute(
        "SELECT DISTINCT category FROM expenses WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])

@app.route("/category_details/<category>")
def category_details(category):

    conn = get_connection()
    cur = conn.cursor()

    data = cur.execute(
        """
        SELECT amount,date
        FROM expenses
        WHERE user_id=? AND category=?
        """,
        (session["user_id"],category)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])

# -------------Monthly Expense ------------

@app.route("/monthly_expense/<month>")
def monthly_expense(month):

    conn = get_connection()
    cur = conn.cursor()

    data = cur.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id=? AND strftime('%m', date)=?
        GROUP BY category
    """, (session["user_id"], month)).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])
#-------------Profile Page -------------

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/")

    conn = get_connection()
    cur = conn.cursor()

    user = cur.execute(
        "SELECT name,email FROM users WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()

    conn.close()

    return render_template("profile.html", user=user)

#------------Update Profile -------------

@app.route("/update_profile", methods=["POST"])
def update_profile():

    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET name=?, email=?
        WHERE user_id=?
    """,(name,email,session["user_id"]))

    conn.commit()
    conn.close()

    return redirect("/profile")

#------------Delete Profile--------------

@app.route("/delete_profile")
def delete_profile():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM expenses WHERE user_id=?",
        (session["user_id"],)
    )

    cur.execute(
        "DELETE FROM users WHERE user_id=?",
        (session["user_id"],)
    )

    conn.commit()
    conn.close()

    session.clear()

    return redirect("/")

#------- Delete expense ----------------
@app.route("/delete_expense/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    conn = get_connection()
    cur = conn.cursor()

    # (Optional safety) ensure the expense belongs to the logged-in user
    cur.execute(
        "DELETE FROM expenses WHERE expense_id=? AND user_id=?",
        (expense_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})
#-----------ADD INCOME -----------------
@app.route("/add_income", methods=["POST"])
def add_income():

    source = request.form["source"]
    amount = request.form["amount"]
    date = request.form["date"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO income(user_id, amount, source, date) VALUES(?,?,?,?)",
        (session["user_id"], amount, source, date)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/balance")
def balance():

    conn = get_connection()
    cur = conn.cursor()

    income = cur.execute(
    "SELECT SUM(amount) FROM income WHERE user_id=?",
    (session["user_id"],)
).fetchone()[0] or 0

    expense = cur.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    conn.close()

    income = income or 0
    expense = expense or 0

    balance = income - expense

    return jsonify({
        "income": income,
        "expense": expense,
        "balance": balance
    })

@app.route("/financial_summary")
def financial_summary():

    if "user_id" not in session:
        return redirect("/")

    return render_template("financial_summary.html")

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)