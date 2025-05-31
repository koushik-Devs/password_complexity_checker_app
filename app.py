from flask import Flask, render_template, request, jsonify
import re
import random
import string

app = Flask(__name__)


def check_password_strength(password):
    suggestions = []

    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        suggestions.append("Include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        suggestions.append("Include at least one lowercase letter.")
    if not re.search(r"\d", password):
        suggestions.append("Include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestions.append("Include at least one special character.")

    if len(password) >= 12 and all([
        re.search(r"[A-Z]", password),
        re.search(r"[a-z]", password),
        re.search(r"\d", password),
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    ]):
        return "Strong", "Your password is strong!", []

    if not suggestions:
        return "Moderate", "Your password is okay but could be stronger.", suggestions
    else:
        return "Weak", "Your password is weak.", suggestions


def generate_strong_password(length=12):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choices(all_chars, k=length))
        strength, _, _ = check_password_strength(password)
        if strength == "Strong":
            return password


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    password = data.get("password", "")
    strength, message, suggestions = check_password_strength(password)
    return jsonify({
        "strength": strength,
        "message": message,
        "suggestions": " ".join(suggestions)
    })


@app.route('/generate')
def generate():
    password = generate_strong_password()
    return jsonify({"password": password})


if __name__ == '__main__':
    app.run(debug=True)
