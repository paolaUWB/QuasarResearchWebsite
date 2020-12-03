
from flask_wtf import Form
from wtforms import StringField, IntegerField, FloatField, SubmitField, FieldList, BooleanField
from wtforms.validators import DataRequired

class DataAccessForm(Form):
    #table 1
    QSO = StringField('QSO')
    Plate_MJD_fiber = StringField('Plate-MJD-fiber')
    ZEMDR9Q = FloatField('ZEMDR9Q')
    ZEMDR9Q_Min = FloatField('ZEMDR9Q_Min')
    ZEMDR9Q_Max = FloatField('ZEMDR9Q_Max')
    ZEMHW10 = FloatField('ZEMHW10')
    ZEMHW10_Min = FloatField('ZEMHW10_Min')
    ZEMHW10_Max = FloatField('ZEMHW10_Max')
    BALQSO = StringField('BALQSO')

    #table 2
    BI_EHVO = IntegerField('BI_EHVO')
    BI_EHVO_min = IntegerField('BI_EHVO_min')
    BI_EHVO_max = IntegerField('BI_EHVO_max')

    V = IntegerField('V')
    V_max = IntegerField('V_max')
    V_min = IntegerField('V_min')

    EW = IntegerField('EW')
    EW_min = IntegerField('EW_min')
    EW_max = IntegerField('EW_max')
    Depth = FloatField('Depth')

    Submit = SubmitField('Filter')
    Download = SubmitField('Download checked data')
