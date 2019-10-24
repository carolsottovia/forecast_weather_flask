# -*- coding: utf-8 -*-
from flask import Flask, render_template
import util

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('table.html', data=util.main())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)