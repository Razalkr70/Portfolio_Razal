# from flask import Flask, render_template, request, 
from flask import Flask, request, render_template, redirect, url_for, flash,jsonify
# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
# import yaml
from flask_mail import Mail, Message
from flask import Flask, request, redirect, flash


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages


# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'razalkrdeveloper@gmail.com'
app.config['MAIL_PASSWORD'] = 'uuvffmxxunjewhhm'  # Paste App Password here

mail = Mail(app)


# # Load YAML data manually
# with open("chatbot.yml", "r", encoding="utf-8") as f:
#     data = yaml.safe_load(f)

# keyword_answers = {}
# for convo in data['conversations']:
#     if isinstance(convo, list) and len(convo) >= 2:
#         question = convo[0].lower()
#         answer = convo[1]
#         keyword_answers[question] = answer

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/get", methods=["POST"])
# def chatbot_response():
#     user_input = request.form["msg"].lower()

    # Sort keywords by length descending to match specific first
    # sorted_keywords = sorted(keyword_answers.keys(), key=len, reverse=True)

    # for keyword in sorted_keywords:
    #     if keyword in user_input:
    #         return jsonify({"response": keyword_answers[keyword]})

    # return jsonify({"response": "Hmm, I might need Razal to teach me that one — could you try asking in a different way?"})



@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('fullname')  # Matching the HTML field name
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

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run(debug=True)
