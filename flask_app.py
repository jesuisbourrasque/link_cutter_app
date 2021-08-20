from flask import Flask, render_template, request, redirect
from db import DB

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html'
    )


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
        return render_template(
            'link.html',
            data=data
        )


@app.route('/short_link/<link>', methods=['GET'])
def get_link(link):
    with DB() as db:
        if data := db.get_link(link):
            return redirect(data, code=302)
        return render_template(
            '404.html'
        ), 404


if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
