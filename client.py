from flask import Flask, render_template

app = Flask(__name__)


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
app.run()
