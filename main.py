from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm, LoginForm, ChoiceForm
from data.users import User
from data.infs import Infs
from data.recs import Recs
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        recs = db_sess.query(Recs).filter(Recs.user_id == current_user.get_id()).all()
        data = []
        if len(recs) > 3:
            recs = recs[-3:]
        for i in recs:
            category = i.category
            genres = i.genres.split(', ')
            mood = i.mood.split(', ')
            for res in db_sess.query(Infs).filter(Infs.category == category):
                res_genres = res.genres.split(', ')
                res_mood = res.mood.split(', ')
                if genres:
                    for genre in genres:
                        if genre in res_genres:
                            data.append((res.title, res.category, res.genres, res.mood, res.summary))
                elif mood:
                    for m in mood:
                        if m in res_mood:
                            data.append((res.title, res.category, res.genres, res.mood, res.summary))
        if len(data) < 3:
            for _ in range(3 - len(data)):
                res = db_sess.query(Infs).first()
                data.append((res.title, res.category, res.genres, res.mood, res.summary))
    else:
        data = []
    return render_template("index2.html", title='Главная страница', data=data)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/films', methods=['GET', 'POST'])
def films():
    form = ChoiceForm()
    if form.validate_on_submit():
        genres = []
        mood = []
        with open('db/genres.txt', mode='w') as file:
            file.write('фильм\n')
            category = 'фильм'
            if form.melodrama.data:
                file.write('мелодрама\n')
                genres.append('мелодрама')
            if form.family.data:
                file.write('семейный\n')
                genres.append('семейный')
            if form.drama.data:
                file.write('драма\n')
                genres.append('драма')
            if form.comedy.data:
                file.write('комедия\n')
                genres.append('комедия')
            if form.horror.data:
                file.write('ужасы\n')
                genres.append('ужасы')
        with open('db/mood.txt', mode='w') as file:
            file.write('фильм\n')
            if form.sadness.data:
                file.write('грусть\n')
                mood.append('грусть')
            if form.joy.data:
                file.write('радость\n')
                mood.append('радость')
            if form.loneliness.data:
                file.write('одиночество\n')
                mood.append('одиночество')
            if form.calmness.data:
                file.write('спокойствие\n')
                mood.append('спокойствие')
            if form.inspiration.data:
                file.write('вдохновлённое\n')
                mood.append('вдохновлённое')
            if form.adrenaline.data:
                file.write('адреналин\n')
                mood.append('адреналин')
        db_sess = db_session.create_session()
        recs = Recs(category=category,
                    genres=', '.join(genres),
                    mood=', '.join(mood),
                    user_id=current_user.get_id())
        db_sess.add(recs)
        db_sess.commit()
        return redirect('/page')
    return render_template('films2.html', title='Фильмы', form=form)


@app.route('/books', methods=['GET', 'POST'])
def books():
    form = ChoiceForm()
    if form.validate_on_submit():
        genres = []
        mood = []
        with open('db/genres.txt', mode='w') as file:
            file.write('книга\n')
            category = 'книга'
            if form.melodrama.data:
                file.write('мелодрама\n')
                genres.append('мелодрама')
            if form.family.data:
                file.write('семейный\n')
                genres.append('семейный')
            if form.drama.data:
                file.write('драма\n')
                genres.append('драма')
            if form.comedy.data:
                file.write('комедия\n')
                genres.append('комедия')
            if form.horror.data:
                file.write('ужасы\n')
                genres.append('ужасы')
        with open('db/mood.txt', mode='w') as file:
            file.write('книга\n')
            category = 'книга'
            if form.sadness.data:
                file.write('грусть\n')
                mood.append('грусть')
            if form.joy.data:
                file.write('радость\n')
                mood.append('радость')
            if form.loneliness.data:
                file.write('одиночество\n')
                mood.append('одиночество')
            if form.calmness.data:
                file.write('спокойствие\n')
                mood.append('спокойствие')
            if form.inspiration.data:
                file.write('вдохновлённое\n')
                mood.append('вдохновлённое')
            if form.adrenaline.data:
                file.write('адреналин\n')
                mood.append('адреналин')
        db_sess = db_session.create_session()
        recs = Recs(category=category,
                    genres=', '.join(genres),
                    mood=', '.join(mood),
                    user_id=current_user.get_id())
        db_sess.add(recs)
        db_sess.commit()
        return redirect('/page')
    return render_template('books.html', title='Книги', form=form)


@app.route('/serial', methods=['GET', 'POST'])
def serial():
    form = ChoiceForm()
    if form.validate_on_submit():
        genres = []
        mood = []
        with open('db/genres.txt', mode='w') as file:
            file.write('сериал\n')
            category = 'сериал'
            if form.melodrama.data:
                file.write('мелодрама\n')
                genres.append('мелодрама')
            if form.family.data:
                file.write('семейный\n')
                genres.append('семейный')
            if form.drama.data:
                file.write('драма\n')
                genres.append('драма')
            if form.comedy.data:
                file.write('комедия\n')
                genres.append('комедия')
            if form.horror.data:
                file.write('ужасы\n')
                genres.append('ужасы')
        with open('db/mood.txt', mode='w') as file:
            file.write('сериал\n')
            category = 'сериал'
            if form.sadness.data:
                file.write('грусть\n')
                mood.append('грусть')
            if form.joy.data:
                file.write('радость\n')
                mood.append('радость')
            if form.loneliness.data:
                file.write('одиночество\n')
                mood.append('одиночество')
            if form.calmness.data:
                file.write('спокойствие\n')
                mood.append('спокойствие')
            if form.inspiration.data:
                file.write('вдохновлённое\n')
                mood.append('вдохновлённое')
            if form.adrenaline.data:
                file.write('адреналин\n')
                mood.append('адреналин')
        db_sess = db_session.create_session()
        recs = Recs(category=category,
                    genres=', '.join(genres),
                    mood=', '.join(mood),
                    user_id=current_user.get_id())
        db_sess.add(recs)
        db_sess.commit()
        return redirect('/page')
    return render_template('serial.html', title='Сериалы', form=form)


@app.route('/page', methods=['GET', 'POST'])
def page():
    with open('db/genres.txt') as file:
        filters1 = list(map(lambda x: x.strip(), file.readlines()))
    with open('db/mood.txt') as file:
        filters2 = list(map(lambda x: x.strip(), file.readlines()))
    db_sess = db_session.create_session()
    data = set()
    for inf in db_sess.query(Infs).filter(Infs.category == filters1[0]):
        genres = inf.genres.split(', ')
        mood = inf.mood.split(', ')
        if filters1[1:]:
            for genre in filters1[1:]:
                if genre in genres:
                    data.add((inf.title, inf.category, inf.genres, inf.mood, inf.summary))
        elif filters2[1:]:
            for m in filters2[1:]:
                if m in mood:
                    data.add((inf.title, inf.category, inf.genres, inf.mood, inf.summary))
        else:
            data.add((inf.title, inf.category, inf.genres, inf.mood, inf.summary))
    return render_template('page.html', title='Рекомендации', data=data)


@app.route('/bad_page', methods=['GET', 'POST'])
def bad_page():
    return render_template('bad_page.html', title='Не выполнен вход в аккаунт')


if __name__ == '__main__':
    main()
