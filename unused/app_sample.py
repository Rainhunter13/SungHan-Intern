from unused.input import username, password, Temp_point_names, Temp_period_name, date
from static.backend import Temp_find_recordings

from flask import Flask, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@app.route('/')
@app.route('/index')
def index_sample():
    user = {"username": "Rakhman"}
    return render_template('index_sample.html', title = 'Welcome Page', user = user)


@app.route('/login/', methods=['GET', 'POST'])
def login_sample():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login_sample.html', title='Sign In', form=form)
    else:
        print(form.username.data)
        print(form.password.data)
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index_sample'))


def authentication():
    return 'login process...'


@app.route('/report/')
def show_data():
    ds = Temp_find_recordings(username, password, Temp_point_names, Temp_period_name, date)
    return ds.to_html(header="true", table_id="table")

@app.route('/urlfor')
def urlfor():
    if True:
        print(url_for('show_data'))
        return show_data()


@app.route('/show_data/<name>/')
def get_name(name):
    return name


@app.route('/show_data/<int:age>')
def get_age(age):
    return age


if __name__ == '__main__':
    app.run()
