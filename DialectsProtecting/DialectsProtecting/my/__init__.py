# encoding: utf-8

from flask import Blueprint

my = Blueprint('my', __name__)

from DialectsProtecting.my import views