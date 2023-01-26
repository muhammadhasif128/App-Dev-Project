@app.route('/userRegister', methods=['GET'])
def user_register1():
    create_user_form = CreateUserFrom(request.form)
    return render_template('newRegister.html')

@app.route('/registerError')
def creation_error():
    # dupe
    return render_template('newRegister.html')

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserFrom(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')
        # email = request.form['email']
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        oList = []
        eList = []
        for key in db:
            user = users_dict.get(key)
            oList.append(user)
            for i in oList:
                eList.append(users_dict[i].get_email_address())

        # user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
        #                  create_user_form.today_date.data, create_user_form.age.data, create_user_form.phone_no.data,
        #                  create_user_form.gender.data, create_user_form.email_address.data,
        #                  create_user_form.postal_code.data, "Default")
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


