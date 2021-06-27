from datetime import datetime
from typing import DefaultDict
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kds_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    bookn = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    cat = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.bookn} - {self.isbn} - {self.cat} - {self.price}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        bookn=request.form['bookn']
        isbn=request.form['isbn']
        cat=request.form['cat']
        price=request.form['price']
        kds_book=Book(bookn=bookn,isbn=isbn,cat=cat,price=price)
        db.session.add(kds_book)
        db.session.commit()

    allBook=Book.query.all()
    return render_template('index.html',allbook=allBook)

@app.route('/about')
def printabout():
    return render_template('about.html')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        bookn=request.form['bookn']
        isbn=request.form['isbn']
        cat=request.form['cat']
        price=request.form['price']
        kds_book=Book.query.filter_by(sno=sno).first()
        kds_book.bookn=bookn
        kds_book.isbn=isbn
        kds_book.cat=cat
        kds_book.price=price
        db.session.add(kds_book)
        db.session.commit()
        return redirect("/")

    ABook=Book.query.filter_by(sno=sno).first()
    return render_template('update.html',book=ABook)

@app.route('/delete/<int:sno>')
def delete(sno):
    ABook=Book.query.filter_by(sno=sno).first()
    db.session.delete(ABook)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,port=8000)
