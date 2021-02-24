from flask import Flask, request, render_template, redirect
from resources import db, SportsGood

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret key'
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def retrieve_all_list():
    goods = SportsGood.query.all()
    return render_template('index.html', goods=goods)


@app.route('/goods/new', methods=['GET', 'POST'])
def create_good():
    good = None

    if request.method == 'POST':
        good_id = request.form['good_id']
        name = request.form['name']
        sport = request.form['sport']
        price = request.form['price']
        good = SportsGood(good_id=good_id, name=name, price=price, sport=sport)
        db.session.add(good)
        db.session.commit()
        return redirect('/')
        # TODO: Tell user that the todo was saved successfully or not

    return render_template('good_form.html', good=good)


@app.route('/goods/<int:good_id>', methods=['GET', 'POST'])
def get_good(good_id):
    good = SportsGood.query.filter_by(good_id=good_id).first()

    if request.method == 'POST':
        if request.form['delete']:
            db.session.delete(good)
            db.session.commit()
            return redirect('/')

        good.name = request.form['name']
        good.sport = request.form['sport']
        good.price = request.form['price']
        db.session.commit()

    return render_template('good_form.html', good=good)


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

