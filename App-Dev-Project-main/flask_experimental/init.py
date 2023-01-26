from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateUserFrom, CreateAdminForm, CreateFoodForm, TopUpUserForm, CreateCardForm, RefillCardForm
import shelve
import User
import Admin
import Menu
import random,string
import Card
# import GetUpdated_ID
import hashlib

app= Flask(__name__)

@app.route('/')
def home():
    return "<h1>" + "Hello" + "</h1>"

@app.route('/createUser', methods=['GET'])
def create_user():
    create_user_form = CreateUserFrom(request.form)
    return render_template('createUser.html', form=create_user_form)

@app.route('/createUser', methods=['POST'])
def checkuser():
    create_user_form = CreateUserFrom(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')
        email = request.form['email']
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")
        oList = []
        eList = []
        for key in db:
            # user = users_dict.get(key)
            # oList.append(user)
            for i in db[key]:
                eList.append(users_dict[i].get_email_address())
        print(eList)
        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                         create_user_form.today_date.data, create_user_form.age.data, create_user_form.phone_no.data,
                         create_user_form.gender.data, create_user_form.email_address.data,
                         create_user_form.postal_code.data, "Default")
        # users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==",
              user.get_user_id())
        global registeredname
        registeredname = user.get_first_name()
        db.close()
        return redirect(url_for('userlogin'))


# @app.route('/registrationError',methods=['GET','POST'])
# def regisWrong():
#     create_user_form = CreateUserFrom(request.form)
#     dupli
#     return render_template('createUser.html', dupli=dupli)


if __name__ == '__main__':
    app.run()
