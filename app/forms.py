
from flask_wtf import Form
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired

class DataAccessForm(Form):
    #table 1
    QSO = StringField('QSO')
    Plate_MJD_fiber = StringField('Plate-MJD-fiber')
    ZEMDR9Q = FloatField('ZEMDR9Q')
    ZEMDR9Q_Min = FloatField('ZEMDR9Q_Min')
    ZEMDR9Q_Max = FloatField('ZEMDR9Q_Max')
    ZEMHW10 = FloatField('ZEMHW10')
    BALQSO = StringField('BALQSO')
    Submit = SubmitField('Submit')