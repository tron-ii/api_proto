import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def  dictionary_b(cursor, row):
    d = {}
    for id_a, col in enumerate(cursor.description):
        d[col[0]] = row[id_a]
    return d


@app.route('/', methods=['GET'])
def home():
     return "<h1>Reading Archive</h1><p> A trivial API for Local Book Database .</p>"


@app.route('/api/v1/resources/books/all', methods=['GET'])
#function retrieves all the data from books.db
def api_all():

     book_db = sqlite3.connect('books.db')
     book_db.row_factory = dictionary_b
     cur = book_db.cursor()
     all_books = cur.execute('SELECT * FROM books;').fetchall()

     return jsonify(all_books)

@app.errorhandler(404)
#Error handling function
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/books', methods=['GET'])
#Enables user to filter using parameters
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published :
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not(id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    book_db= sqlite3.connect('books.db')
    book_db.row_factory = dictionary_b
    cur = book_db.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
