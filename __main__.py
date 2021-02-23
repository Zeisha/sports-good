from flask import Flask, request, render_template, redirect, flash
from resources import db, SportsGoodInventory

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret key'
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/app/')
def retrieve_all_list():
    goods = SportsGoodInventory.query.all()
    print(goods)
    return render_template('index.html', goods=goods)


@app.route('/app/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create_form.html')

    if request.method == 'POST':
        good_id = request.form['good_id']
        name = request.form['name']
        sport = request.form['sport']
        price = request.form['price']
        good = SportsGoodInventory(good_id=good_id, name=name, price=price, sport=sport)
        db.session.add(good)
        db.session.commit()
        flash("Sport good added successfully")
        return redirect('/app/')


@app.route('/app/<int:good_id>')
def retrieve_good(good_id):
    good = SportsGoodInventory.query.filter_by(good_id=good_id).first()
    if good:
        return render_template('good_detailed_view.html', good=good)
    return f"Sport good  with id ={good_id} does not exist"


@app.route('/app/<int:good_id>/update', methods=['GET', 'POST'])
def update(good_id):
    good = SportsGoodInventory.query.filter_by(good_id=good_id).first()
    if request.method == 'GET':
        # TODO: You should not have multiple forms for basically the same: create, update, show
        return render_template('update_form.html', good=good)
    if request.method == 'POST':
        if good:
            good.name = request.form['name']
            good.sport = request.form['sport']
            good.price = request.form['price']
            db.session.commit()
            flash("Good updated successfully")
            return redirect(f'/app/{good_id}')
        return f"Sport good  with id ={good_id} does not exist"


@app.route('/app/<int:good_id>/delete', methods=['GET', 'POST'])
def delete(good_id):
    good = SportsGoodInventory.query.filter_by(good_id=good_id).first()
    if good:
        db.session.delete(good)
        db.session.commit()
        return redirect('/app')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
