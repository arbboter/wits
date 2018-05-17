# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as vd


class TestCaseIdForm(FlaskForm):
    id = wtforms.IntegerField('用例ID', validators=[vd.data_required()])
