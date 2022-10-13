from crypt import methods
from email.mime import image
import os
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SECRET_KEY'] = '89e6d4081e714ff217e1918572ceb858'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app) 

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable = False)
    phone = db.Column(db.String(100))
    matric_number  = db.Column(db.String(20), nullable = False)
    date_of_birth = db.Column(db.String(100), nullable = False)
    image = db.Column(db.String(20), nullable = False)
    

    def __init__(self, name, email, phone, matric_number, date_of_birth, image):
        self.name = name
        self.email = email
        self.phone = phone
        self.matric_number = matric_number
        self.date_of_birth = date_of_birth
        self.image = image
        
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}', {self.matric_number}, {self.date_of_birth}, {self.image})"
        


@app.route("/")
def Index():
    all_data = Student.query.all()
    
    return render_template('index.html', students = all_data)

@app.route("/insert", methods=['POST'])
def insert():
    
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        matric_number = request.form['matric_number']
        date_of_birth = request.form['date_of_birth']
        image = request.form['image']
        
        
        my_data = Student(name, email, phone, matric_number, date_of_birth, image)
        db.session.add(my_data)
        db.session.commit()
        
        flash(f'Congrats fellow, your information has been added succesfully.', 'success')
        
        return redirect(url_for('Index'))
    
@app.route("/update", methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('id'))   
        
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.matric_number = request.form['matric_number']
        my_data.phone = request.form['date_of_birth']
        my_data.image = request.form['image']
        
        
        
        db.session.commit()
        flash("Your info has been updated successfully.", "success")
        
        return redirect(url_for('Index'))
        
@app.route("/view")
def view():
    students = Student.query.all()
    return render_template('view.html', students=students )

@app.route("/delete/<id>", methods= ['GET', "POST"])
def delete(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student info deleted successfully.", "success")
    
    return redirect(url_for('Index')) 
        

if __name__ == "__main__":
    app.run(debug=True) 