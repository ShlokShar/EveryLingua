from packages.models import *
from packages.backend import *

# APPLICATION AND DATABASE SETUP
app = flask.Flask(__name__)
app.secret_key = "shlok"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database.init_app(app)

with app.app_context():
    database.create_all()
    pass


# GETTERS
@app.route('/')
def home():
    if flask.session.get("email"):
        user = Users.query.filter_by(email=flask.session.get("email")).first()
        print(user.recent_language)
        if user.recent_language:
            return flask.redirect("/learn/" + user.recent_language)
        else:
            return flask.redirect("/add-language")
    return flask.render_template("index.html")


@app.route("/learn/<language>")
@logged_in
def dashboard(language):
    user = Users.query.filter_by(email=flask.session.get("email")).first()
    if language in list(user.languages):
        user.recent_language = language
        database.session.commit()
        return flask.render_template(f"/languages/{language}.html", languages=user.languages, selected=language)
    return flask.redirect("/")


@app.route("/add-language")
@logged_in
def add_language():
    languages = base_languages
    user = Users.query.filter_by(email=flask.session.get("email")).first()
    user_languages = user.languages
    available_languages = {key: value for key, value in languages.items() if key not in user_languages}

    return flask.render_template("main/add_language.html", languages=available_languages)


@app.route("/remove-language")
@logged_in
def remove_language():
    user = Users.query.filter_by(email=flask.session.get("email")).first()
    user_languages = user.languages
    return flask.render_template("main/remove_language.html", languages=user_languages)


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]

        user = Users.query.filter_by(email=email).first()
        if user and user.password == password:
            flask.session["email"] = email
            flask.session.permanent = True
            return flask.redirect("/")
        else:
            return flask.render_template("login.html", error="Account does not exist or invalid credentials")
    else:
        if flask.session.get("email"):
            return flask.redirect("/")
        else:
            return flask.render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if flask.request.method == "POST":
        if not flask.request.form.get("email") or len(flask.request.form.get("password")) < 8:
            return flask.render_template("signup.html",
                                         error="Please input a valid email and a password with 8 characters or more.")

        email = flask.request.form["email"]
        password = flask.request.form["password"]
        user = Users(email, password)

        database.session.add(user)
        database.session.commit()
        flask.session["email"] = email
        flask.session.permanent = True

        return flask.redirect("/")
    else:
        if flask.session.get("email"):
            return flask.redirect("/")
        else:
            return flask.render_template("signup.html")


# SETTERS
@app.route("/add/<language>")
def add(language):
    if flask.session.get("email"):
        user = Users.query.filter_by(email=flask.session.get("email")).first()
        if language in list(base_languages.keys()) and language not in list(user.languages.keys()):
            languages = dict(user.languages)

            languages[language] = {
                "flag": base_languages[language]["flag"],
                "chat-logs": {},
                "grammar": {
                    "scores": [],
                    "suggestions": []
                },
                "vocabulary": {
                    "scores": [],
                    "suggestions": []
                },
                "phrases": {
                    "scores": [],
                    "suggestions": []
                },
                "culture": {
                    "scores": [],
                    "suggestions": []
                }
            }

            user.languages = languages
            user.recent_language = language
            database.session.commit()

            return "1"
        else:
            return "0"
    else:
        return "-1"


@app.route("/remove/<language>")
def remove(language):
    if flask.session.get("email"):
        user = Users.query.filter_by(email=flask.session.get("email")).first()
        if language in list(user.languages.keys()):
            languages = dict(user.languages)
            languages.pop(language)
            user.languages = languages

            if len(user.languages) == 0:
                user.recent_language = ""
            else:
                user.recent_language = random.choice(list(user.languages.keys()))
            database.session.commit()
            return "1"
        else:
            return "0"
    else:
        return "-1"


@app.route("/get-grammar/<difficulty>/<concepts>/<language>")
def get_grammar(difficulty, concepts, language):
    practice_problems = grammar(10, difficulty=difficulty, concepts=concepts, language=language)
    random.shuffle(practice_problems)
    print(practice_problems)
    return flask.jsonify(practice_problems)


@app.route("/get-vocabulary/<difficulty>/<concepts>/<language>")
def get_vocabulary(difficulty, concepts, language):
    practice_problems = vocabulary(10, difficulty, concepts, language)
    random.shuffle(practice_problems)
    print(practice_problems)
    return flask.jsonify(practice_problems)


@app.route("/get-culture/<difficulty>/<concepts>/<language>")
def get_culture(difficulty, concepts, language):
    practice_problems = culture(10, difficulty, language, concepts)
    random.shuffle(practice_problems)
    print(practice_problems)
    return flask.jsonify(practice_problems)


@app.route("/learn/send-text/<text>/<language>")
def send_text(text, language):
    text = text.replace("%%", " ")
    print(text)
    response = chatbot(text, language)
    return flask.jsonify(response)


if __name__ == '__main__':
    app.run()
