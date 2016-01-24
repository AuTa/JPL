# coding: utf-8

from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.fields.html5 import URLField, DateTimeField
from wtforms.validators import DataRequired, URL
from wtforms import ValidationError
# from.models import BookMark


class KanaForm(Form):
    kanamoji = StringField('Press Space Start', validators=[DataRequired()])
    render_time = HiddenField()
    submit_time = HiddenField()

    # def validate_url(self, field):
    #     if BookMark.query.filter_by(url=field.data).first():
    #         raise ValidationError('URL already added.')
