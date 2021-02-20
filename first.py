from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "Привет, Яндекс!"


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

if __name__ == '__main__':
    app.run(debug=True)
