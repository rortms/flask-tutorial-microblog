from flask import Flask
from config import Config

myapp = Flask(__name__)
myapp.config.from_object(Config)

from app import routes, forms

