from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

    def __init__(self, doctorName, doctorEmail):
        self.doctorName = doctorName
        self.doctorEmail = doctorEmail

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
    doctor = db.relationship('Doctors', backref=db.backref('doctor', lazy=True))

    areaId = db.Column(db.Integer, db.ForeignKey('location.areaid'), nullable = False)
    location = db.relationship('Location', backref=db.backref('location', lazy=True))

    def __init__(self, patientName):
        self.patientName = patientName
    
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
    doctor = db.relationship('patient', backref=db.backref('patient', lazy=True))

    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return f"<Payment {self.amount}>"
