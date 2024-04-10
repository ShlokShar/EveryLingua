from packages.imports import *


class Users(database.Model):
    _id = database.Column("id", database.Integer, primary_key=True)
    email = database.Column(database.String(100))
    password = database.Column(database.String(100))

    languages = database.Column(database.JSON)
    is_premium = database.Column(database.Boolean, default=False)
    recent_language = database.Column(database.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.languages = {}
        self.recent_language = ""
