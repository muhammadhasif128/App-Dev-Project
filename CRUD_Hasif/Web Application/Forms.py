from wtforms import Form, StringField, RadioField, validators, EmailField, DateField, IntegerField
from datetime import datetime

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
