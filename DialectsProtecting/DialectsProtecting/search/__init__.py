# encoding: utf-8

from flask import Blueprint

search = Blueprint('search', __name__)

from DialectsProtecting.search import views
