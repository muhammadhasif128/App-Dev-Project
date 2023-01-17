from wtforms import Form, StringField, RadioField, validators, EmailField, DateField, IntegerField,FloatField
from datetime import datetime
from dateutil.relativedelta import relativedelta

class CreateUserFrom(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter Last Name"})
    today_date = DateField('Registration Date', default=datetime.today)
    age = IntegerField('Age', render_kw={"placeholder": "Enter Your Age"})
    phone_no = StringField('Phone Number', [validators.Length(max=8), validators.DataRequired()], render_kw={"placeholder": "+65"})
    gender = RadioField('Gender', choices=[("M", "Male"), ("F", "Female")], render_kw={"placeholder": "Enter Your Gender"})
    email_address = EmailField("Email Address", [validators.InputRequired()], render_kw={"placeholder": "Enter your email, eg:. example@gmail.com"})
    postal_code = IntegerField("Postal Code", [validators.NumberRange(min=0, max=999999)], render_kw={"placeholder": "Enter your 6 digit postal code"})
    account_status = StringField('Account Status', default="Administrator", render_kw={'readonly': True})

class CreateAdminForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter Last Name"})
    today_date = DateField('Registration Date', default=datetime.today)
    age = IntegerField('Age', render_kw={"placeholder": "Enter Your Age"})
    phone_no = StringField('Phone Number', [validators.Length(max=8), validators.DataRequired()], render_kw={"placeholder": "+65"})
    gender = RadioField('Gender', choices=[("M", "Male"), ("F", "Female")], render_kw={"placeholder": "Enter Your Gender"})
    email_address = EmailField("Email Address", [validators.InputRequired()], render_kw={"placeholder": "Enter your email: example@gmail.com"})
    account_status = StringField('Account Status', default="Administrator", render_kw={'readonly': True})

class CreateFoodForm(Form):
    food_type = RadioField('Category', choices=[("Burger", "Burger"), ("Sides", "Sides"), ("Drinks", "Drinks")])
    food_name = StringField('Food Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter First Name"})
    food_price = FloatField('Price',[validators.NumberRange(min=1, max=100), validators.DataRequired()], render_kw={"placeholder": "Enter Food Price"})
    image_name = StringField('Image Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter Image"})

class RefillCardForm(Form):
    enter_code = StringField('Enter your unique code ID : ', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter Code"})
    token_amt = IntegerField("Top Up Amount", [validators.NumberRange(min=0, max=999999)], render_kw={"placeholder": "Enter Amount of tokens to top up"})



class TopUpUserForm(Form):
    top_up_amt = IntegerField("Top Up Amount", [validators.NumberRange(min=0, max=999999)], render_kw={"placeholder": "Enter Amount to top up"})
    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter Last Name"})

class CreateCardForm(Form):
    name = StringField('Full Name', [validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Enter Name"})
    email_address = EmailField("Email Address", [validators.InputRequired()], render_kw={"placeholder": "Enter your email, eg:. example@gmail.com"})
    date_created = DateField('Registration Date', default = datetime.today, render_kw={'readonly':True})
    lifespan = IntegerField('Lifespan (years)', default=6,render_kw={'readonly' : True})
    expiry_date = DateField('Card expires on : ', default=(datetime.today() + relativedelta(years = 6)),render_kw={'readonly' : True})
