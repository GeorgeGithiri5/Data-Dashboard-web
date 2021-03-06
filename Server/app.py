from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import plotly
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:george@localhost/HealthTech'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret-me'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Doctors(db.Model):

    __tablename__ = 'doctors'

    doctorId = db.Column(db.Integer, primary_key=True)
    doctorName = db.Column(db.String(80), nullable=False)
    doctorEmail = db.Column(db.String(80), nullable = False)
    doctorSpeciality = db.Column(db.String(60), nullable=False)

    def __init__(self, doctorName, doctorEmail, doctorSpeciality):
        self.doctorName = doctorName
        self.doctorEmail = doctorEmail
        self.doctorSpeciality = doctorSpeciality

    def __repr__(self):
        return f"<Doctor {self.doctorName}>"
    

class Patient(db.Model):

    __tablename__ = 'patient'

    patientid = db.Column(db.Integer, primary_key=True)
    patientName = db.Column(db.String(200), nullable=False)
    patientPhone = db.Column(db.String(30), unique = True, nullable=False)
    patientSex = db.Column(db.String(40), nullable = True)
    patientIllness = db.Column(db.String(50), nullable = True)
    patientAge = db.Column(db.Integer, nullable=True)

    doctorId = db.Column(db.Integer, db.ForeignKey('doctors.doctorId'), nullable=False)
    doctor = db.relationship('Doctors', backref=db.backref('doctors', lazy=True))

    areaId = db.Column(db.Integer, db.ForeignKey('location.areaid'), nullable = False)
    location = db.relationship('Location', backref=db.backref('location', lazy=True))

    def __init__(self, patientName, patientPhone, patientSex, patientIllness, patientAge, doctorId, areaId):
        self.patientName = patientName
        self.patientPhone = patientPhone
        self.patientSex = patientSex
        self.patientIllness = patientIllness
        self.patientAge = patientAge
        self.doctorId = doctorId
        self.areaId = areaId

    
    def __repr__(self):
        return f"<Patient {self.patientName}>"

class Location(db.Model):

    __tablename__ = 'location'

    areaid = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(80), nullable=False)

    def __init__(self, area):
        self.area = area

    def __repr__(self):
        return f"<Location {self.area}>"


class Payment(db.Model):

    __tablename__ = 'payment'

    paymentId = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable = False)
    paymentMethod = db.Column(db.String(80), nullable=False)

    patientId = db.Column(db.Integer, db.ForeignKey('patient.patientid'), nullable=False)
    doctor = db.relationship('Patient', backref=db.backref('Patient', lazy=True))

    def __init__(self, amount, paymentMethod, patientId):
        self.amount = amount
        self.paymentMethod = paymentMethod
        self.patientId = patientId


    def __repr__(self):
        return f"<Payment {self.amount}>"


# Develop Apis
# patient
@app.route('/patient', methods = ['POST', 'GET'])
def patient():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_patient = Patient(
                patientName=data['patientName'],
                patientPhone = data['patientPhone'],
                patientSex = data['patientSex'],
                patientIllness = data['patientIllness'],
                patientAge = data['patientAge'],
                doctorId = data['doctorId'],
                areaId = data['areaId']
                )
            db.session.add(new_patient)
            db.session.commit()
            return {"message": f"Patient {new_patient.patientName} has been added"}
        else:
            return {"error":"The request payload is not in Json format"}

    elif request.method == 'GET':
        patients = Patient.query.all()
        results = [
            {
                "name":patient.patientName,
                "phone": patient.patientPhone,
                "Sex":patient.patientSex,
                "Illness":patient.patientIllness,
                "Age":patient.patientAge,
                "doctorId": patient.doctorId,
                "areaId":patient.areaId
            } for patient in patients
        ]
        dataJson = json.dumps(results)

        df = pd.read_json(dataJson)
        print(df)
        fig = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[df.name, df.phone, df.Illness],
                        fill_color='lavender',
                        align='left'))
            ])
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('index.html', graphJSON=graphJSON)

# Doctor API
@app.route('/doctor', methods = ['POST', 'GET'])
def doctor():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_doctor = Doctors(
                doctorName=data['doctorName'],
                doctorEmail=data['doctorEmail'],
                doctorSpeciality = data['doctorSpeciality']
            )
            db.session.add(new_doctor)
            db.session.commit()

            return {"Message": f"Doctor {new_doctor.doctorName} has been added"}
        else:
            return {"error":"The Request payload is not in Json Format"}

    elif request.method == 'GET':
        doctors = Doctors.query.all()
        output = [
            {
                "Name":doctor.doctorName,
                "Email":doctor.doctorEmail,
                "Speciality":doctor.doctorSpeciality
            } for doctor in doctors
        ]  
        return jsonify(output)

# Location API
@app.route('/location', methods=['POST', 'GET'])
def location():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_loaction = Location(
                area= data['area']
            )
            db.session.add(new_loaction)
            db.session.commit()

            return {"Message": f"{new_loaction.area} was added successfully!"}
        else:
            return {"error":"The request payload is not in JSON Format"}
    elif request.method == 'GET':
        areas = Location.query.all()
        output = [
            {
                "Area": location.area
            } for location in areas
        ]
        return jsonify(output)

# Payment API
@app.route('/payment', methods=['POST', 'GET'])
def payment():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_payment = Payment(
                amount=data["amount"],
                paymentMethod=data["paymentMethod"],
                patientId=data["patientId"]
            )
            db.session.add(new_payment)
            db.session.commit()

            return {"Message": f"Payment Made Successfully"}
        else:
            return {"error":"The request payload is not in JSON format"}

    elif request.method == 'GET':
        payments = Payment.query.all()
        output = [{
                "Amount":payment.amount,
                "paymentMethod":payment.paymentMethod,
                "patientId": payment.patientId
            }for payment in payments]
       
        dataJson = json.dumps(output)

        # to_list = eval(dataJson)

        df = pd.read_json(dataJson)
        fig = px.bar(data_frame=df, x = df['paymentMethod'], y=df['Amount'], color=df['patientId'])
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        # print(graphJSON)
        
        return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)