from flask import Flask, render_template
import threading
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sqlite3
app = Flask(__name__)
URL,PORT = 'localhost',1518

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tables-data')
def tables_data():
    return render_template('tables-data.html')


@app.route('/forms-basic')
def forms_basic():
    return render_template('forms-basic.html')


@app.route('/forms-advanced')
def forms_advanced():
    return render_template('forms-advanced.html')


@app.route('/page-login')
def page_login():
    return render_template('page-login.html')


@app.route('/page-register')
def page_register():
    return render_template('page-register.html')


@app.route('/pages-forget.html')
def pages_forget():
    return render_template('pages-forget.html')


# {{ url_for('page_register') }}
if __name__ == '__main__':
    thread = threading.Thread(target=app.run, args=[URL, PORT])
    thread.daemon = True
    thread.start()
    qt_app = QApplication([])
    w = QWebEngineView()
    w.setWindowTitle('My Browser')

    w.load(QUrl('http://%s:%s'%(URL, PORT)))
    w.showMaximized()
    w.show()
    qt_app.exec_()
