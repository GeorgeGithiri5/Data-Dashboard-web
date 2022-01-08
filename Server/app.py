from flask import Flask, request, jsonify
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

    def __init__(self, amount):
        self.amount = amount

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
        return jsonify(results)

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




if __name__ == '__main__':
    app.run(debug=True)