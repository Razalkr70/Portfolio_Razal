from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
from flask_mail import Mail, Message
from rapidfuzz import fuzz
import yaml
from operator import itemgetter
import datetime

app = Flask(__name__)
app.secret_key = 'portfolio1'  # Required for session and flashing messages

# ================= MAIL CONFIG ===================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'razalkrdeveloper@gmail.com'
app.config['MAIL_PASSWORD'] = 'uuvffmxxunjewhhm'  # Use Gmail App Password

mail = Mail(app)

# ================= YAML CHATBOT LOADER ===================
with open("chatbot.yml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

keyword_answers = {}
for convo in data['conversations']:
    if isinstance(convo, list) and len(convo) >= 2:
        *question_variants, answer = convo
        for q in question_variants:
            keyword_answers[q.lower()] = answer

def get_best_match(user_input, keyword_answers, threshold=80):
    candidates = []
    for keyword in keyword_answers:
        score = fuzz.partial_ratio(user_input, keyword)
        if score >= threshold:
            candidates.append((keyword, score, len(keyword.split())))
    if not candidates:
        return None
    candidates.sort(key=itemgetter(1, 2), reverse=True)
    return candidates[0][0]

def log_chat(user, bot):
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        now = datetime.datetime.now()
        f.write(f"{now} - USER: {user}\n")
        f.write(f"{now} - BOT: {bot}\n")


# ================= ROUTES ===================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"].lower()
    match = get_best_match(user_input, keyword_answers)
    if match:
        response = keyword_answers[match]
        session['last_topic'] = match
        log_chat(user_input, response)
        return jsonify({"response": response})

    last_topic = session.get("last_topic")
    if last_topic:
        if "project" in last_topic and "more" in user_input:
            response = "Razal has also worked on Facial Emotion Detection, AI Thought Bubble Generator, and Palm Line Reader AI."
            log_chat(user_input, response)
            return jsonify({"response": response})

    default_response = "Hmm, I might need Razal to teach me that one — could you try asking in a different way?"
    log_chat(user_input, default_response)
    return jsonify({"response": default_response})

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('fullname')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("All fields are required.", "danger")
            return redirect(url_for('contact'))

        msg = Message('New Contact Message',
                      sender='razalkrdeveloper@gmail.com',
                      recipients=['razalkrdeveloper@gmail.com'])
        msg.body = f"From: {name} <{email}>\n\n{message}"

        try:
            mail.send(msg)
            return redirect(url_for('contact', success='true'))
        except Exception as e:
            print("Send Mail Error:", e)
            flash('Failed to send message. Please try again later.', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html')

# ================= RUN ===================
if __name__ == "__main__":
    app.run(debug=True)
