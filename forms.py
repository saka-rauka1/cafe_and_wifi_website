from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField
from wtforms.validators import DataRequired, Length


# Create Form
class CafeForm(FlaskForm):
    name = StringField("Cafe Name:", validators=[DataRequired(), Length(max=250)])
    map_url = URLField("Map URL:", validators=[DataRequired(), Length(max=500)])
    img_url = URLField("Image URL:", validators=[DataRequired(), Length(max=500)])
    location = StringField("Location:", validators=[DataRequired(), Length(max=250)])
    has_sockets = BooleanField("Has Sockets:")
    has_toilet = BooleanField("Has Toilet:")
    has_wifi = BooleanField("Has Wifi:")
    can_take_calls = BooleanField("Can Take Calls:")
    seats = StringField("Number of Seats:", validators=[Length(max=250)])
    coffee_price = StringField("Coffee Price:", validators=[Length(max=250)])
    submit = SubmitField("Add Cafe")


class DeleteForm(FlaskForm):
    name = StringField("Cafe Name:", validators=[DataRequired(), Length(max=250)])
    submit = SubmitField("Delete Cafe")
