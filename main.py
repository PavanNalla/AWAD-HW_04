from multiprocessing.sharedctypes import Value
import os
import re
from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, RadioField, SelectField, TextAreaField
from flask import Flask
from wtforms.validators import DataRequired, InputRequired
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__, template_folder="")
app.config['SECRET_KEY'] = 'hw_04'
app. config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app. config[ 'SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class newuser(db.Model):
    __tablename__ = "newuser"

    id= db.Column(db.Integer, primary_key=True)
    companyname= db.Column(db.Text)
    phone= db.Column(db.Integer)
    email= db.Column(db.Text)
    address= db.Column(db.Text)

    def __init__ (self, companyname, phone, email, address):
        self.companyname=companyname
        self.phone=phone
        self.email=email
        self.address=address   

    def __repr__(self):
        return f'{self.id}-{self.companyname}-{self.phone}-{self.email}-{self.address}'
    

class MyForm(FlaskForm):
    companyname = StringField('Company Name:')
    phone = StringField('Phone:')
    email = StringField('Email:')
    address = StringField('Address:')
    ID = StringField('ID:')
    
@app.route('/', methods=['GET', 'POST'])
def index():     
    form = MyForm()
    if request.method == 'POST':
            if request.form['submit'] == 'add above record':
                cname = form.companyname.data
                phone = form.phone.data
                email = form.email.data
                address = form.address.data
                if cname != None and phone != None and email != None and address != None:
                    db.create_all()
                    db.session.add_all([newuser(form.companyname.data,form.phone.data,form.email.data,form.address.data)])
                    db.session.commit()  
                    form.companyname.process_data(' ')
                    form.phone.process_data(' ')
                    form.email.process_data(' ')
                    form.address.process_data(' ')
            elif request.form['submit'] == 'show all records':
                return redirect(url_for('greet'))
    return render_template ('home.html', form = form)

@app.route('/greet', methods=['GET', 'POST'])
def greet():     
    form = MyForm()
    if request.method == 'POST':
        if request.form['submit'] == 'delete this record':
            phone_data=request.form.get('phone')
            record = newuser.query.filter_by(phone = phone_data).first()
            db.session.delete(record)
            db.session.commit()  
            form.ID.process_data(' ')
            return render_template ('results.html', x = newuser.query.all() ) 
        elif request.form['submit'] == 'Update record':
            phone_data=request.form.get('phone')
            print(phone_data)
            record = newuser.query.filter_by(phone = phone_data).first()
            return redirect(url_for('add', ab = phone_data))
    return render_template ('results.html', x = newuser.query.all() )  


@app.route('/add', methods=['GET', 'POST'])
def add():     
    a = request.args.get('ab')
    print(a)
    if request.method == 'POST':
        print('b')
        if request.form['submit'] == 'update':
            print('c')
            change_user = newuser.query.filter(newuser.phone == a).first()
            print(change_user)
            change_user.companyname = request.form.get('companyname')
            change_user.phone = request.form.get('phone')
            change_user.email = request.form.get('email')
            change_user.address = request.form.get('address')
            db.session.add(change_user)
            db.session.commit()
            return redirect(url_for('greet', x = newuser.query.all() ) )
    return render_template ('add.html')   

      
if __name__ == '__main__':
    app.run(debug=True)
    



