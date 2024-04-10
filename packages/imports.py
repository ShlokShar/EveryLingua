import flask
import string
import re
import openai
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import random

database = SQLAlchemy()
