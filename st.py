from flask import Flask, render_template, url_for, request, jsonify, session, flash, redirect, send_file



app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random string'

@app.route('/')
def index():
    return render_template('index.html', side_pos='active')







if __name__ == '__main__':
    app.run(debug=True)