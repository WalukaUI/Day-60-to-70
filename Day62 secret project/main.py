from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location URL', validators=[DataRequired(), URL()])
    cafe_open_time = StringField('Cafe open time, eg: 8.30am', validators=[DataRequired()])
    cafe_closing_time = StringField('Cafe closing time, eg: 5.30pm', validators=[DataRequired()])
    cafe_coffee_rating = SelectField('Cafe coffee rating', choices=[('☕️'), ('☕️☕️'), ('☕️☕️☕️'),('☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    cafe_wifi_rating = SelectField('Cafe wifi rating', choices=[('✘'),('💪'), ('💪💪'), ('💪💪💪'),('💪💪💪💪'),('💪💪💪💪💪')], validators=[DataRequired()])
    cafe_power_outlet_rating = SelectField('Cafe power outlet rating', choices=[('✘'),('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    form = CafeForm()
    if form.validate_on_submit():
        newline=[form.cafe.data,form.cafe_location.data,form.cafe_open_time.data,form.cafe_closing_time.data,form.cafe_coffee_rating.data, form.cafe_wifi_rating.data, form.cafe_power_outlet_rating.data]
        print(newline)
        with open('cafe-data.csv', mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.cafe_location.data},"
                           f"{form.cafe_open_time.data},"
                           f"{form.cafe_closing_time.data},"
                           f"{form.cafe_coffee_rating.data},"
                           f"{form.cafe_wifi_rating.data},"
                           f"{form.cafe_power_outlet_rating.data}")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
