# under venv folder

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask("__name__")

formData = {}


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        lastName = request.form['lname']
        firstName = request.form['fname']
        formData['lastName'] = lastName
        formData['firstName'] = firstName
        return redirect(url_for('output'))
    else:
        return render_template('home.html')


@app.route("/output")
def output():
    return render_template('output.html', name=formData['firstName'])


if __name__ == "__main__":
    app.run(debug=True)
