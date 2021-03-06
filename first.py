from flask import Flask, url_for, request, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from data import db_session
from data.users import User
from Занятия.flasksite.data.news import News

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LKfkhds872w98feihw'


class Form(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Пароль')
    submit = SubmitField('Отправить')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


@app.route('/')
def index():
    return render_template('base.html', title='Заголовок')


@app.route('/child')
def child():
    return render_template('page.html', title='Расширяющий')


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = Form()
    if form.validate_on_submit():
        return form.name.data + ' ' + form.email.data + ' ' + form.password.data
    return render_template('form.html', form=form)


@app.route('/count')
def countdown():
    a = []
    for i in range(10, 0, -1):
        a.append(i)
    return str(a)


@app.route('/img')
def image():
    return f'''
    <img src='{ url_for('static', filename='img/ovtsa.png')}'>
    '''


@app.route('/css', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return '''
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Крутая страница</title>
                <alink rel="stylesheet" href="static/css/style.css">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
            </head>
            <body>
            <h1> Заголовок </h1>
            <p>Точно по такому же принципу работает и остальной статический контент. Давайте рассмотрим еще один пример: сделаем обработчик return_sample_page, который вернет пользователю нашу первую HTML-страницу, сверстанную по всем правилам:</p>
            <p>А теперь давайте добавим css-файл, который заменит цвет текста на красный. Для этого создадим в папке css внутри папки со статическим контентом файл style.css со следующим текстом:</p>
            <form method="post" enctype="multipart/form-data">
            <input type='text' name='text'><br>
            <button type="submit" class="btn btn-primary">Отправить</button>
            </form>
            </body>
            </html>
        '''
    else:
        return request.form['text']


@app.route('/greeting/<username>')
def greeting(username):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                   <link rel="stylesheet"
                   href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                   integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                   crossorigin="anonymous">
                    <title>Привет, {username}</title>
                  </head>
                  <body>
                    <h1>Привет, {username}!</h1>
                  </body>
                </html>'''


@app.route("/news")
def news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')

    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    # добавление в таблицу
    # user = User()
    # user.name = 'Пользователь 3'
    # user.about = 'Не любит'
    # user.email = 'dontlike@ya.ru'
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()
    # выборка
    # db_sess = db_session.create_session()
    # users = db_sess.query(User).filter(User.id > 1).all()
    # print(users)
    # изменение
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).filter(User.id == 1).first()
    # user.name = 'Суперпользователь 1'
    # db_sess.commit()
    # db_sess = db_session.create_session()
    # news = News(title="Первая новость", content="Привет блог!",
    #             user_id=1, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()
    app.run(debug=True)
