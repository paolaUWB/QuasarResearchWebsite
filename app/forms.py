
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


    # example = BooleanField('Label')
    # string_of_files = ['one\r\ntwo\r\nthree\r\n']
    # list_of_qausars = string_of_files[0].split()
    # # create a list of value/description tuples
    # files = [(x, x) for x in list_of_files]
    # example = MultiCheckboxField('Label', choices=files)
    Submit = SubmitField('Submit')
    Download = SubmitField('Download checked data')

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()




# class ExampleForm(Form):
#     user = QuerySelectMultipleField(
#         'User',
#         query_factory=lambda: User.query.all(),
#         widget=widgets.ListWidget(prefix_label=False),
#         option_widget=widgets.CheckboxInput()
#     )
#     submit = SubmitField('Submit')
# def file_list_form_builder(filenames):
#     for (i, filename) in enumerate(filenames):
#         setattr(DataAccessForm, 'filename_%d' % i, BooleanField(label=download))

#     return FileListForm()