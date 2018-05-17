# -*- coding: utf-8 -*-
from flask import Blueprint

org_blueprint = Blueprint('org', __name__)

from . import views