from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

db = SQLAlchemy(app)

# ================= MODELS =================

class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    author = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return self.title

# ================= ROUTES =================

@app.route('/')
def home():

    books = Book.query.all()

    return render_template(
        'books.html',
        books=books
    )

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']

        new_book = Book(
            title=title,
            author=author,
            category=category,
            quantity=quantity
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect('/')

    return render_template('add_book.html')

@app.route('/delete/<int:id>')
def delete_book(id):

    book = Book.query.get_or_404(id)

    db.session.delete(book)
    db.session.commit()

    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_book(id):

    book = Book.query.get_or_404(id)

    if request.method == 'POST':

        book.title = request.form['title']
        book.author = request.form['author']
        book.category = request.form['category']
        book.quantity = request.form['quantity']

        db.session.commit()

        return redirect('/')

    return render_template(
        'update_book.html',
        book=book
    )

# ================= MAIN =================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
