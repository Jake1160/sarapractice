# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, NumberRange
from wtforms.fields.html5 import URLField, DateField, IntegerRangeField, EmailField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, RadioField
from wtforms_components import TimeField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')


class WorkoutForm(FlaskForm):
    excercise = StringField('Excercise', validators=[DataRequired()])
    weight = StringField('Weight', validators=[DataRequired()])
    sets = StringField('sets', validators=[DataRequired()])
    reps = StringField('reps', validators=[DataRequired()])
    submit = SubmitField('Track!')