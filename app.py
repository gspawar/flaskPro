from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    age = db.Column(db.String(500), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.fullname}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        fullname = request.form['fullname']
        age = request.form['age']
        mobile = request.form['mobile']
        user = User(fullname=fullname, age=age, mobile=mobile)
        db.session.add(user)
        db.session.commit()

    allUser = User.query.all()
    return render_template('index.html', allUser=allUser)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        fullname = request.form['fullname']
        age = request.form['age']
        mobile = request.form['mobile']
        user = User.query.filter_by(sno=sno).first()
        user.fullname = fullname
        user.age = age
        user.mobile = mobile
        db.session.add(user)
        db.session.commit()
        return redirect("/")

    user = User.query.filter_by(sno=sno).first()
    return render_template('update.html', user=user)


@app.route('/delete/<int:sno>')
def delete(sno):
    user = User.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)