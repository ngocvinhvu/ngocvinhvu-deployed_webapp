from flask import Flask, render_template, url_for
import sqlite3


conn = sqlite3.connect('familug.db', check_same_thread=False)
c = conn.cursor()


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/awesomejobs")
def awesomejobs():
    c.execute('SELECT * FROM awe_jobs')
    return render_template('awesome-jobs.html', title='awesome-jobs', rows = c.fetchall())


@app.route("/familug")
def familug():
    return render_template('familug.html', title='familug', rows = c.fetchall())


@app.route("/familug/python")
def python():
	c.execute('SELECT * FROM fami_python')
	return render_template('python.html', title='python', rows = c.fetchall())


@app.route("/familug/command")
def command():
	c.execute('SELECT * FROM fami_command')
	return render_template('command.html', title='command', rows = c.fetchall())


@app.route("/familug/sysadmin")
def sysadmin():
	c.execute('SELECT * FROM fami_sysadmin')
	return render_template('sysadmin.html', title='sysadmin', rows = c.fetchall())


@app.route("/familug/lastest")
def lastest():
	c.execute('SELECT * FROM fami_lastest')
	return render_template('lastest.html', title='lastest', rows = c.fetchall())


if __name__ == '__main__':
    app.run(debug=True)