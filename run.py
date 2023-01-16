from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserFrom, CreateAdminForm, CreateFoodForm
import shelve
import User
import Admin
import Menu

app = Flask(__name__)

formData ={}

@app.route('/')
def home():
    return render_template('LoginPage.html')

@app.route('/userpage')
def user():
    return render_template('index.html')


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
    admin_dict = {}
    db = shelve.open('admin.db', 'r')
    admin_dict = db['Staff']
    db.close()
    admin_list = []
    for key in admin_dict:
        admin = admin_dict.get(key)
        admin_list.append(admin)


    return render_template('AdminHomePage.html', count=len(admin_list), admin_list=admin_list)

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
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

        return redirect(url_for('successreg'))
    return render_template('createUser.html', form=create_user_form)

@app.route('/createFood', methods=['GET','POST'])
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
        return redirect(url_for('home'))
    return render_template('createFood.html', form=create_food_form)

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
        return redirect(url_for('home'))
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
                            create_admin_form.email_address.data)
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
    return redirect(url_for('retrieve_staff'))



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
    users_dict.pop(id)
    db['Users'] = users_dict
    db.close()
    return redirect(url_for('retrieve_users'))


if __name__ == '__main__':
    app.run()
