from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

formData ={}

@app.route('/')
def home():
    return render_template('LoginPage.html')

@app.route('/userpage')
def user():
    return render_template('index.html')


@app.route("/form", methods=['POST', 'GET'])
def userreg():
    if request.method == 'POST':
        lastName = request.form['lname']
        firstName = request.form['fname']
        formData['lastName'] = lastName
        formData['firstName'] = firstName
        return redirect(url_for('output'))
    else:
        return render_template('form.html')


@app.route("/output")
def output():
    return render_template('output.html', name=formData['firstName'])

@app.route('/forget')
def forget():
    return render_template('password.html')

@app.route('/admin')
def admin():
    return render_template('AdminLogin.html')

@app.route('/adminpage')
def adminpage():
    return render_template('AdminHomePage.html')

if __name__ == '__main__':
    app.run()