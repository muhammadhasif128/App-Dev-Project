from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserFrom, TopUpUserForm, CreateCardForm, RefillCardForm
import random,string
import shelve
import User
import Card


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

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
        create_user_form.today_date.data, create_user_form.age.data, create_user_form.phone_no.data, create_user_form.gender.data, create_user_form.email_address.data, create_user_form.postal_code.data, "Default")
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==", user.get_user_id())
        global registeredname
        registeredname = user.get_first_name()

        db.close()

        return redirect(url_for('successreg'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/successreg', methods=['GET', 'POST'])
def successreg():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('output.html', registeredname = registeredname)

@app.route('/createAdmin', methods=['GET', 'POST'])
def create_admin():
    create_user_form = CreateUserFrom(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
        create_user_form.today_date.data, create_user_form.age.data, create_user_form.phone_no.data, create_user_form.gender.data, create_user_form.email_address.data, create_user_form.postal_code.data, create_user_form.account_status.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==", user.get_user_id())
        global registeredname
        registeredname = user.get_first_name()

        db.close()

        return redirect(url_for('successreg'))
    return render_template('createAdmin.html', form=create_user_form)


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


        card = Card.Card(create_card_form.name.data, digitcode, create_card_form.date_created.data, create_card_form.lifespan.data, create_card_form.expiry_date.data, create_card_form.email_address.data)
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

        return redirect(url_for('successreg'))
    return render_template('createCard.html', form=create_card_form, digitcode = digitcode)

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
        return redirect(url_for('retrieve_card'))
    else:
        return render_template('refillCard.html',form = refill_card_form)


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

        return redirect(url_for('retrieve_users'))
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



@app.route('/updateCard/<int:id>/', methods=['GET', 'POST'])
def update_card(id):
    update_card_form = CreateCardForm(request.form)
    if request.method == 'POST' and update_card_form.validate():
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

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']
    users_dict.pop(id)
    db['Users'] = users_dict
    db.close()
    return redirect(url_for('retrieve_users'))

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
