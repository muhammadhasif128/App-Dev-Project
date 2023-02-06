from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserFrom, CreateAdminForm, CreateFoodForm, TopUpUserForm, CreateCardForm, RefillCardForm,CreateFeedbackForm
import pandas as pd
import shelve
import User
import Admin
import Menu
import random,string
import Card
import GetUpdated_ID
import Feedback

app = Flask(__name__)
formData ={}

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/aboutpage')
def about():
    return render_template('about.html')

@app.route('/userlogin', methods=['GET'])
def userlogin1():
    return render_template('LoginPage.html')

# @app.route('/typo', methods=['GET'])
# def incorrect():
#     return render_template('LoginIncorrectPage.html')


@app.route('/typoadmin', methods=['GET'])
def adminincorrect():
    return render_template('AdminIncorrectPage.html')


@app.route('/userlogin', methods=['GET','POST'])
def userlogin():
    if request.method == "POST":
        # Get the form data
        email = request.form["email"]

        user_dict = {}
        db = shelve.open('user.db', 'r')
        user_dict = db['Users']
        db.close()
        user_list = []
        aList=[]
        pList=[]
        for key in user_dict:
            user = user_dict.get(key)
            user_list.append(user)
        for i in user_list:
            # print(i.get_email_address())
            # print(i.get_password())
            aList.append(i.get_email_address())
            pList.append(i.get_password())
            if str(i.get_email_address()) == email:
                global loginname
                loginname = i.get_first_name()
                break
        print(aList)
        print(pList)

        password = request.form["password"]
        if email in aList:
            cpass = aList.index(email)
            if password == pList[cpass]:
                print("Login Successful")
                return redirect(url_for('user'))
            else:
                global typo
                typo = 'Email or Password incorrect'
                return render_template('LoginPage.html', typo=typo)
        else:
            print('Email or Password incorrect')
            typo = 'Email or Password incorrect'
            return render_template('LoginPage.html', typo=typo)
    return render_template('LoginPage.html')



@app.route('/userpage', methods=['GET', 'POST'])
def user():
    loginname
    createfeedback = CreateFeedbackForm(request.form)
    if request.method == 'POST':
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db['Feedback']
        except:
            print('Error in retrieving Feedback from feedback.db')

        feedback = Feedback.Feedback(createfeedback.feedback.data)
        feedback_dict[feedback.get_ID()] = feedback
        db['Feedback'] = feedback_dict

        # Test Code
        feedback_dict = db['Feedback']
        feedback = feedback_dict[feedback.get_ID()]
        print(f"New feedback was stored in feedback.db with feedback_ID == {feedback.get_ID()}")
        db.close()
        global sClear
        sClear = "Feedback successfully submitted"
        return render_template('index.html', loginname=loginname, form=createfeedback, sClear=sClear)

    return render_template('index.html',loginname=loginname, form=createfeedback)


@app.route('/adminusers')
def adminusers():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('AdminHomePageUsers.html', count=len(users_list), users_list=users_list)

@app.route('/adminreports')
def adminreports():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db['Feedback']
    db.close()
    f_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        f_list.append(feedback)

    return render_template('AdminHomePageReports.html', count=len(f_list), f_list=f_list)

@app.route('/exportFeedback')
def export_feedback():

    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db['Feedback']
    db.close()

    df = pd.DataFrame()


    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        df = df.append({'User ID': feedback.get_ID(),
                        'Feedback Description': feedback.get_feedback()
                        },
                        ignore_index=True)


    df.to_excel('feedback.xlsx', index=False)

    return redirect(url_for('adminreports'))

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

# @app.route("/admin", methods=['GET'])
# def admin1():
#     return render_template('AdminLogin.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        # Get the form data
        email = request.form["email"]

        admin_dict = {}
        db = shelve.open('admin.db', 'r')
        admin_dict = db['Staff']
        db.close()
        admin_list = []
        for key in admin_dict:
            admin = admin_dict.get(key)
            admin_list.append(admin)
        for i in admin_list:
            print(i.get_email_address())
            if str(i.get_email_address())==str(email):
                global loginname 
                loginname = i.get_first_name()
                break
        try:
            print(loginname)
        except NameError:
            typo = 'Email or Password is incorrect, please try again.'
            print("Invalid Login Email.")
            return render_template('AdminLogin.html',typo=typo)

        password = request.form["password"]
        if password == "Fastburg12345!":
            print("Login Successful")
            return redirect(url_for('adminpage'))
        else:
            print("Incorrect Details")
            typo = 'Email or Password is incorrect, please try again.'
            return render_template('AdminLogin.html',typo=typo)
    return render_template('AdminLogin.html')

@app.route('/adminpage')
def adminpage():
    loginname
    admin_dict = {}
    db = shelve.open('admin.db', 'r')
    admin_dict = db['Staff']
    db.close()
    admin_list = []
    for key in admin_dict:
        admin = admin_dict.get(key)
        admin_list.append(admin)

    return render_template('AdminHomePage.html', count=len(admin_list), admin_list=admin_list, loginname=loginname)

# @app.route('/createUser', methods=['GET'])
# def create_user():
#     create_user_form = CreateUserFrom(request.form)
#     return render_template('createUser.html', form=create_user_form)

@app.route('/createUser', methods=['GET','POST'])
def create_user():
    create_user_form = CreateUserFrom(request.form)
    if request.method == 'POST' and create_user_form.validate():
            users_dict = {}
            db = shelve.open('user.db', 'c')

            email = request.form['email_address']
            try:
                users_dict = db['Users']
            except:
                print("Error in retrieving Users from user.db.")
            eList=[]
            iList =[]
            for key in users_dict:
                mail = users_dict.get(key)
                eList.append(key)

            for i in users_dict:
                nid = users_dict[i].get_user_id()
                iList.append(nid)
                if str(email) == str(users_dict[i].get_email_address()):
                    global typo
                    typo = "Email already in use"
                    return render_template('createUser.html',typo=typo, form=create_user_form)
                    break

            user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                             create_user_form.today_date.data, create_user_form.age.data, create_user_form.phone_no.data,
                             create_user_form.gender.data, create_user_form.email_address.data, create_user_form.user_password.data,
                             create_user_form.postal_code.data, "Default")

            # uh = GetUpdated_ID.Ufunction() + 1
            # user.set_user_id(uh)
            users_dict[user.get_user_id()] = user
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
    return render_template('createUser.html', form=create_user_form)


# @app.route('/registrationError',methods=['GET','POST'])
# def regisWrong():
#     create_user_form = CreateUserFrom(request.form)
#     dupli
#     return render_template('createUser.html', dupli=dupli)

@app.route('/userRegister', methods=['GET', 'POST'])
def user_register():
    create_user_form = CreateUserFrom(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                         create_user_form.today_date.data, create_user_form.age.data, create_user_form.phone_no.data,
                         create_user_form.gender.data, create_user_form.email_address.data,
                         create_user_form.postal_code.data, "Default")
        users_dict[user.get_user_id()] = user
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
    return render_template('newRegister.html', form=create_user_form)

# @app.route('/createUser', methods=['GET'])
# def user_register1():
#     create_user_form = CreateUserFrom(request.form)
#     return render_template('createUser.html', form=create_user_form)

# @app.route('/registerError',methods=['POST'])
# def creation_error():
#     dupe
#     return render_template('createUser.html', dupe=dupe)





@app.route('/createFood', methods=['GET', 'POST'])
def create_food():
    create_food_form = CreateFoodForm(request.form)
    if request.method == 'POST' and create_food_form.validate():
        food_dict = {}
        db = shelve.open('food.db', 'c')

        try:
            food_dict = db['Food']
        except:
            print("Error in retrieving Food from food.db.")

        food = Menu.Food(create_food_form.food_type.data, create_food_form.food_name.data,
                         create_food_form.food_price.data,
                         create_food_form.image_name.data)
        food_dict[food.get_food_id()] = food
        db['Food'] = food_dict

        food_dict = db['Food']
        food = food_dict[food.get_food_id()]
        print(food.get_name(), "was stored in food.db successfully with food_id ==", food.get_food_id())

        db.close()
        return redirect(url_for('userlogin'))
    return render_template('createFood.html', form=create_food_form)

@app.route('/Menu')
def menu():
    loginname
    # 2 items each category
    food_list = ['Chicken Burger', 'Beef Burger', 'French Fries', 'Potato Wedges',
                 'Coke', 'Smoothie']
    reco = food_list[random.randint(0, 5)]

    return render_template('order_menu.html', reco=reco, loginname=loginname)

@app.route('/retrieveFood')
def retrieve_food():
    food_dict = {}
    db = shelve.open('food.db', 'r')
    food_dict = db['Food']
    db.close()

    food_list = []
    for key in food_dict:
        food = food_dict.get(key)
        food_list.append(food)

    return render_template('retrieveFood.html', count=len(food_list), food_list=food_list)


@app.route('/deleteFood/<int:id>', methods=['POST'])
def delete_food(id):
    food_dict = {}
    db = shelve.open('food.db', 'w')
    food_dict = db['Food']
    id += 1
    food_dict.pop(id)
    db['Food'] = food_dict
    db.close()
    return redirect(url_for('retrieve_food'))


@app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
def update_food(id):
    update_food_form = CreateFoodForm(request.form)
    if request.method == 'POST' and update_food_form.validate():
        food_dict = {}
        db = shelve.open('food.db', 'w')
        food_dict = db['Food']

        food = food_dict.get(id)
        food.set_food_type(update_food_form.food_type.data)
        food.set_name(update_food_form.food_name.data)
        food.set_price(update_food_form.food_price.data)
        food.set_image(update_food_form.image_name.data)

        db['Food'] = food_dict
        db.close()

        return redirect(url_for('retrieve_food'))
    else:
        food_dict = {}
        db = shelve.open('food.db', 'r')
        food_dict = db['Food']
        db.close()
        food = food_dict.get(id)
        update_food_form.food_type.data = food.get_food_type()
        update_food_form.food_name.data = food.get_name()
        update_food_form.food_price.data = food.get_price()
        update_food_form.image_name.data = food.get_image()

        return render_template('updateFood.html', form=update_food_form)


@app.route('/successreg', methods=['GET', 'POST'])
def successreg():
    if request.method == 'POST':
        return redirect(url_for('userlogin'))
    return render_template('output.html', registeredname=registeredname)


@app.route('/createAdmin', methods=['GET', 'POST'])
def create_admin():
    create_admin_form = CreateAdminForm(request.form)
    if request.method == 'POST' and create_admin_form.validate():
        admin_dict = {}
        db = shelve.open('admin.db', 'c')

        try:
            admin_dict = db['Staff']
        except:
            print("Error in retrieving Staff from staff.db.")

        admin = Admin.Admin(create_admin_form.first_name.data, create_admin_form.last_name.data,
                            create_admin_form.today_date.data, create_admin_form.age.data,
                            create_admin_form.phone_no.data, create_admin_form.gender.data,
                            create_admin_form.email_address.data, create_admin_form.admin_password.data)
        # admin.set_staff_id(GetUpdated_ID.Sfunction()+1)
        admin_dict[admin.get_staff_id()] = admin
        db['Staff'] = admin_dict

        # Test codes
        admin_dict = db['Staff']
        admin = admin_dict[admin.get_staff_id()]
        print(admin.get_first_name(), admin.get_last_name(), "was stored in staff.db successfully with user_id ==",
              admin.get_staff_id())
        global registeredname
        registeredname = admin.get_first_name()

        db.close()

        return redirect(url_for('successreg'))
    return render_template('createAdmin.html', form=create_admin_form)


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/retrieveStaff')
def retrieve_staff():
    admin_dict = {}
    db = shelve.open('admin.db', 'r')
    admin_dict = db['Staff']
    db.close()

    admin_list = []
    for key in admin_dict:
        admin = admin_dict.get(key)
        admin_list.append(admin)
    return render_template('retrieveStaff.html', count=len(admin_list), admin_list=admin_list)

@app.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
def update_staff(id):
    update_staff_form = CreateAdminForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        admin_dict = {}
        db = shelve.open('admin.db', 'w')
        admin_dict = db['Staff']

        admin = admin_dict.get(id)
        admin.set_first_name(update_staff_form.first_name.data)
        admin.set_last_name(update_staff_form.last_name.data)
        admin.set_gender(update_staff_form.gender.data)
        admin.set_today_date(update_staff_form.today_date.data)
        admin.set_age(update_staff_form.age.data)
        admin.set_phone_no(update_staff_form.phone_no.data)
        admin.set_email_address(update_staff_form.email_address.data)

        db['Staff'] = admin_dict
        db.close()

        return redirect(url_for('adminpage'))
    else:
        admin_dict = {}
        db = shelve.open('admin.db', 'r')
        admin_dict = db['Staff']
        db.close()
        user = admin_dict.get(id)
        update_staff_form.first_name.data = user.get_first_name()
        update_staff_form.last_name.data = user.get_last_name()
        update_staff_form.gender.data = user.get_gender()
        update_staff_form.today_date.data = user.get_today_date()
        update_staff_form.age.data = user.get_age()
        update_staff_form.phone_no.data = user.get_phone_no()
        update_staff_form.email_address.data = user.get_email_address()
        return render_template('updateStaff.html', form=update_staff_form)


@app.route('/deleteStaff/<int:id>', methods=['POST'])
def delete_staff(id):
    admin_dict = {}
    db = shelve.open('admin.db', 'w')
    admin_dict = db['Staff']
    admin_dict.pop(id)
    db['Staff'] = admin_dict
    db.close()
    return redirect(url_for('adminpage'))



@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserFrom(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_today_date(update_user_form.today_date.data)
        user.set_age(update_user_form.age.data)
        user.set_phone_no(update_user_form.phone_no.data)
        user.set_email_address(update_user_form.email_address.data)
        user.set_postal_code(update_user_form.postal_code.data)
        user.set_account_status(update_user_form.account_status.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('adminusers'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()
        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.today_date.data = user.get_today_date()
        update_user_form.age.data = user.get_age()
        update_user_form.phone_no.data = user.get_phone_no()
        update_user_form.email_address.data = user.get_email_address()
        update_user_form.postal_code.data = user.get_postal_code()
        update_user_form.account_status.data = user.get_account_status()
        return render_template('updateUser.html', form=update_user_form)





@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']
    print(users_dict[id].get_user_id())
    users_dict.pop(id)
    db['Users'] = users_dict
    db.close()
    return redirect(url_for('adminusers'))


@app.route('/createCard', methods=['GET', 'POST'])
def create_card():
    create_card_form = CreateCardForm(request.form)
    '''def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    digitcode = random_with_N_digits(10)'''
    digitcode = ''.join(random.choices(string.ascii_letters.upper() + string.digits, k=16))
    if request.method == 'POST' and create_card_form.validate():
        card_dict = {}
        db = shelve.open('card.db', 'c')

        try:
            card_dict = db['Card']
        except:
            print("Error in retrieving Users from card.db.")


        card = Card.Card(create_card_form.name.data,create_card_form.lastname.data, digitcode,
                         create_card_form.date_created.data, create_card_form.lifespan.data,
                         create_card_form.expiry_date.data,create_card_form.email_address.data)
        card_dict[card.get_counter()] = card
        db['Card'] = card_dict

        '''# Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==", user.get_user_id())
        global registeredname
        registeredname = user.get_first_name()

        db.close()'''
        global registeredname
        registeredname = card.get_name()

        return redirect(url_for('user'))
    return render_template('createCard.html', form=create_card_form, digitcode=digitcode)

@app.route('/retrieveCard')
def retrieve_card():
    db = shelve.open('card.db','r')
    card_dict = db['Card']
    db.close()

    card_list = []

    for id in card_dict:
        card = card_dict.get(id)
        card_list.append(card)

    return render_template('retrieveCardInfo.html', count = len(card_list),card_list=card_list)


@app.route('/refillCard',methods=['GET', 'POST'])
def refill_card():
    refill_card_form = RefillCardForm(request.form)
    if request.method == 'POST' and refill_card_form.validate():

        card_dict = {}
        db = shelve.open('card.db', 'w')

        try:
            card_dict = db['Card']
        except:
            print("Error in retrieving Users from card.db.")

        for id in card_dict:
           card = card_dict.get(id)
           if card.get_card_id() == refill_card_form.enter_code.data:
               #update credit
               card.set_tokens(refill_card_form.token_amt.data)
               db['Card'] = card_dict
               db.close()
        return redirect(url_for('user'))
    else:
        return render_template('refillCard.html',form = refill_card_form)


@app.route('/topUpUser/<int:id>', methods = ['GET','POST'])
def top_up_user(id):
    top_up_form = TopUpUserForm(request.form)
    if request.method == 'POST' and top_up_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_account_credit(top_up_form.top_up_amt.data)
        user.set_first_name(top_up_form.first_name.data)
        user.set_last_name(top_up_form.last_name.data)
        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        user = users_dict.get(id)
        top_up_form.top_up_amt.data = user.get_account_credit()
        top_up_form.first_name.data = user.get_first_name()
        top_up_form.last_name.data = user.get_last_name()
        db.close()
        user = users_dict.get(id)
        current_credit = user.get_account_credit()
        return render_template('topUpUser.html', form=top_up_form, current_credit=current_credit)

@app.route('/updateCard/<int:id>/', methods=['GET', 'POST'])
def update_card(id):
    update_card_form = CreateCardForm(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('card.db', 'w')
        card_dict = db['Card']

        user = card_dict.get(id)
        user.set_name(update_card_form.name.data)
        user.set_email(update_card_form.email_address.data)

        db['Card'] = card_dict
        db.close()

        return redirect(url_for('retrieve_card'))
    else:
        card_dict = {}
        db = shelve.open('card.db', 'r')
        card_dict = db['Card']
        db.close()
        user = card_dict.get(id)
        update_card_form.name.data = user.get_name()
        update_card_form.email_address.data = user.get_email()

        return render_template('updateCard.html', form=update_card_form)

@app.route('/deleteCard/<int:id>', methods=['POST'])
def delete_card(id):
    card_dict = {}
    db = shelve.open('card.db', 'w')
    card_dict = db['Card']
    card_dict.pop(id)
    db['Card'] = card_dict
    db.close()
    return redirect(url_for('retrieve_card'))




if __name__ == '__main__':
    app.run()
