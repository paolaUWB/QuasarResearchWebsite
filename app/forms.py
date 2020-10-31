
from flask_wtf import Form
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

class DataAccessForm(Form):
    #table 1
    QSO = StringField('QSO')
    Plate_MJD_fiber = StringField('Plate-MJD-fiber')
    BI_EHVO = IntegerField('BI_EHVO')
    V_max = IntegerField('V_max')
    V_min = IntegerField('V_min')
    EW = IntegerField('EW')
    Depth = FloatField('Depth')