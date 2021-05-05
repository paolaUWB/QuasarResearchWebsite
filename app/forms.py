# TITLE: Forms
# CONTRIBUTORS: Kathleen Guinee, Audrey Nguyen
# DESCRIPTION: Contains the forms for the website

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SubmitField, FieldList, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

# Search form for the data access page
class DataAccessForm(FlaskForm):
    #table 1
    QSO = StringField('QSO')
    Plate = IntegerField('Plate')
    Plate_Min = IntegerField('Plate_Min')
    Plate_Max = IntegerField('Plate_Max')
    MJD = IntegerField('MJD')
    MJD_Min = IntegerField('MJD_Min')
    MJD_Max = IntegerField('MJD_Max')
    Fiber = IntegerField('Fiber')
    Fiber_Min = IntegerField('Fiber_Min')
    Fiber_Max = IntegerField('Fiber_Max')
    ZEMDR9Q = FloatField('zₑₘ (DR9Q)')
    ZEMDR9Q_Min = FloatField('ZEMDR9Q_Min')
    ZEMDR9Q_Max = FloatField('ZEMDR9Q_Max')
    ZEMHW10 = FloatField('zₑₘ (HW10)')
    ZEMHW10_Min = FloatField('ZEMHW10_Min')
    ZEMHW10_Max = FloatField('ZEMHW10_Max')
    BALQSO_YES = BooleanField('Yes')
    BALQSO_NO = BooleanField('No')

    #table 2
    BI_EHVO = IntegerField('BIₑₕᵥₒ')
    BI_EHVO_min = IntegerField('BI_EHVO_min')
    BI_EHVO_max = IntegerField('BI_EHVO_max')

    V = IntegerField('v')
    V_max = IntegerField('V_max')
    V_min = IntegerField('V_min')

    EW = IntegerField('EW')
    EW_min = IntegerField('EW_min')
    EW_max = IntegerField('EW_max')
    Depth = FloatField('Depth')

    Submit = SubmitField('Filter')
    Download = SubmitField('Download checked data')

# Login form for the website
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')