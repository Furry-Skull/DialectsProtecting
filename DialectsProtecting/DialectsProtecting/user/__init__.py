# encoding: utf-8

from flask import Blueprint

user = Blueprint('user', __name__)

from DialectsProtecting.user import views
from DialectsProtecting.user import userUtils