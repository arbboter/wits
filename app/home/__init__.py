# -*- coding: utf-8 -*-
from flask import Blueprint

home_blueprint = Blueprint('home', __name__)

from . import views
from . import errors