from flask import Flask, render_template, url_for, request, jsonify, session, flash, redirect, send_file



app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random string'

@app.route('/', methods=['GET', 'POST'])
def search():
    return render_template('search.html', side_pos='active')


@app.route('/card_user', methods=['GET', 'POST'])
def card_user():
    return render_template('card_user.html', side_pos='active')


@app.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('data.html', side_pos='active')

@app.route('/export', methods=['GET', 'POST'])
def export():
    return render_template('export.html', side_pos='active')


if __name__ == '__main__':
    app.run(debug=True)