from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login_spindle_id = StringField('Spindle ID (decimal)', validators=[DataRequired()])
    login_spindle_key = PasswordField('Spindle Key', validators=[DataRequired()])
    submit = SubmitField('Login')

class TimespanForm(FlaskForm):
    timespan_select = SelectField(u'View', choices=[('3', '3 days'), ('7', '7 days'), ('14', '14 days'), ('21', '21 days')])

class NameChangeForm(FlaskForm):
    new_spindle_name = StringField('New Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class DataDeleteForm(FlaskForm):
    delete_data = BooleanField('Confirm deletion of all mesaurement data (iSpindel key will not be deleted)')
    submit = SubmitField('Delete')