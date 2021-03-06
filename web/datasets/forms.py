from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
#from wtforms import Form
from web import utils


class DatasetForm(FlaskForm):
    dataset_name = utils.forms.StringField(u'Dataset Name',
                                           validators=[DataRequired()]
                                           )