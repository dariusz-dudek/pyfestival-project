from sanic import Sanic, Blueprint
from sanic.response import json
from pymongo import MongoClient


app = Sanic("library")

bp = Blueprint('my_blueprint')


@bp.listener('before_server_start')
async def setup_connection(app, loop):
    global client
    client = MongoClient(
        'localhost',
        27017,
        username='root',
        password='example'
    )


@bp.listener('after_server_stop')
async def close_connection(app, loop):
    print('Bay bay!')
    await client.close()


@app.route("/books", methods=['GET'])
async def get_books(request):
    print(request)
    db = client['library']
    books = db['books'].find()
    return json([{'title': book['title'], 'author': book['author']} for book in books])


@app.route("/books", methods=['POST'])
async def add_book(request):
    db = client['library']
    books = db['books']
    book = request.json
    book_id = books.insert_one(book).insrted_id
    return json({'id': str(book_id)})


if __name__ == "__main__":
    app.blueprint(bp)
    app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
