from flask import Flask, render_template, request, redirect
from db import DB

app = Flask(__name__)
with DB() as db:
    db.create_schema()


@app.route('/')
def index():
    return render_template(
        'index.html'
    )


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.route('/short_link', methods=['POST'])
def post_links():
    long_link = request.form.get('long_link')
    short_link = request.form.get('short_link')
    if not long_link:
        return render_template(
            'index.html',
            attention='Please enter long url'
        )
    with DB() as db:
        data = db.post_links(long_link, short_link)
        if not data:
            data = 'such a short link already exists'
        else:
            data = f'your short link - {short_link}'
        return render_template(
            'link.html',
            data=data
        )


@app.route('/short_link/<link>', methods=['GET'])
def get_link(link):
    with DB() as db:
        if data := db.get_link(link):
            return redirect(data, code=302)
        return page_not_found()


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


app.run(debug=True, host='0.0.0.0')
