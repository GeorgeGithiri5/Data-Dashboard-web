
-- Create Doctor Table: This is the only table with no Foreign Key For now

CREATE TABLE Doctor(
	doctorId SERIAL Primary Key,
	doctorName VARCHAR(200),
	doctorEmail VARCHAR(200),
	doctorSpeciality VARCHAR(200)
);

INSERT INTO Doctor (doctorName, doctorEmail, doctorSpeciality) VALUES
	('Alfred Kimani', 'alfkimani@gmail.com', 'Dentist'),
	('George Githiri', 'alfkimani@gmail.com', 'Dentist')

-- This is simple Location Table Script

Create Table PatientLocation(
	areaId SERIAL PRIMARY KEY,
	area VARCHAR(200)
);

INSERT INTO PatientLocation(
	area
) Values
	('Rongai'),
	('Kiamumbi')

