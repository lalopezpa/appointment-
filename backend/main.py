from fastapi import FastAPI, HTTPException, Path
from sqlalchemy import create_engine, text
from typing import List
from schemas import Patient, Doctor, Schedule,Service, Appointment, IPS, Medicament_avaliable, Medicament,MedicamentDetail
from models import patients, doctors, schedules, Base, services, appointments, ips,med_avaliability, medicaments

app = FastAPI()

db_user = "admin"        
db_pass = "password"     
db_host = "postgres"    
db_port = 5432         
db_name = "rasi"         


engine = create_engine(
    f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
    echo=True
)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

from fastapi.middleware.cors import CORSMiddleware


# GET
# GET ALL
@app.get("/patients", response_model=List[Patient])
def getPatients():
    with engine.connect() as c:
        result =c.execute(text("SELECT * FROM patients"))
        return result.all()
@app.get("/ips", response_model=List[IPS])
def getIPSs():
    with engine.connect() as c:
        result =c.execute(text("SELECT * FROM ips"))
        return result.all()
    
@app.get("/medicaments", response_model=List[Medicament])
def getMedicaments():
    with engine.connect() as c:
        stmt = medicaments.select()
        result =c.execute(stmt)
        return result.all()
    
@app.get("/doctors", response_model=List[Doctor]) 
def getDoctors():
    with engine.connect() as c: 
        stmt = doctors.select()
        result = c.execute(stmt).all()
        return result
    
@app.get("/services", response_model=List[Service]) 
def getServices():
    with engine.connect() as c: 
        stmt = services.select()
        result = c.execute(stmt).all()
        return result
@app.get("/schedules", response_model=List[Schedule]) 
def getSchedules():
    with engine.connect() as c: 
        stmt = schedules.select()
        result = c.execute(stmt).all()
        return result
@app.get("/appointments", response_model=List[Appointment]) 
def getAppointments():
    with engine.connect() as c: 
        stmt = appointments.select()
        result = c.execute(stmt).all()
        return result
    
    
# GET ONE 
@app.get("/patients/{id}", response_model=Patient)
def getPatient(id: int):
    with engine.connect() as c: 
            stmt = patients.select().where(patients.c.id == id)
            result = c.execute(stmt).fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Patient not found")
            return result
@app.get("/ips/{id}", response_model=IPS)
def getIPS(id: int):
    with engine.connect() as c:  
            stmt = ips.select().where(ips.c.id == id)
            result = c.execute(stmt).fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="IPS not found")
            return result
@app.get("/medicaments/{id}", response_model=Medicament) 
def getMedicament(id: int):
    with engine.connect() as c: 
            stmt = medicaments.select().where(medicaments.c.id == id)
            result = c.execute(stmt).fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Medicament not found")
            return result

@app.get("/ips/{id_ips}/medicaments", response_model=List[MedicamentDetail]) 
def getMedsAvaliability(id_ips: int):
    with engine.connect() as c: 
        stmt = "SELECT * FROM medicaments_avaliable  LEFT JOIN MEDICAMENTS ON MEDICAMENTS.ID = medicaments_avaliable.ID_MEDICAMENT  WHERE id_ips = " + str(id_ips) 
        result = c.execute(text(stmt)).all()
        
        return result      
        
@app.get("/doctors/{id}", response_model=Doctor) 
def getDoctor(id: int):
    with engine.connect() as c: 
        stmt = doctors.select().where(doctors.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return result

@app.get("/appointments/{id}", response_model=Appointment) 
def getAppointment(id: int):
    with engine.connect() as c: 
        stmt = appointments.select().where(appointments.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return result

@app.get("/services/{id}", response_model=Service) 
def getService(id: int):
    with engine.connect() as c: 
        stmt = services.select().where(services.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Service not found")
        return result

@app.get("/ips/{id_ips}/medicaments/{id_medicament}", response_model=MedicamentDetail) 
def getMedAvaliability(id_ips: int, id_medicament: int):
    with engine.connect() as c: 
        stmt = "SELECT * FROM medicaments_avaliable  LEFT JOIN MEDICAMENTS ON MEDICAMENTS.ID = medicaments_avaliable.ID_MEDICAMENT  WHERE id_ips = " + str(id_ips) + " AND id_medicament = " +str(id_medicament)  
        result = c.execute(text(stmt)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Medicament not found")
        return result
    
@app.get("/medicaments/{id_medicament}/ips", response_model=IPS) 
def getMedIPS( id_medicament: int):
    with engine.connect() as c: 
        stmt = "SELECT * FROM medicaments_avaliable  LEFT JOIN IPS ON IPS.ID = medicaments_avaliable.ID_IPS  WHERE id_medicament = " + str(id_medicament) 
        result = c.execute(text(stmt)).fetchone()
        return result
# POST 
@app.post("/patients")
def addPatient(patient: Patient ):
    patientd = { 
                'id': patient.id,
                'name': patient.name,
                'birth': patient.birth,
                'gender': patient.gender,
                'pnumber': patient.pnumber,
                'email': patient.email
    }
    with engine.connect() as c:
        try:
            getPatient(patient.id)
            return "Cannot create Patient, already exists"
        except HTTPException as e:
            c.execute(patients.insert().values(patientd))
            c.commit()
            return patientd

@app.post("/ips")
def addIPS(ipss: IPS ):
    ipsd = { 
                'id': ipss.id,
                'name': ipss.name,
                'pnumber': ipss.pnumber,
                'email': ipss.email,
                'address':ipss.address 
    }
    with engine.connect() as c:
        try:
            getIPS(ipss.id)
            return "Cannot create IPS, already exists"
        except HTTPException as e:
            c.execute(ips.insert().values(ipsd))
            c.commit()
            return ipsd
        
@app.post("/medicaments")
def addMedicament(medicament: Medicament ):
    medicamentd = { 
                'id': medicament.id,
                'name': medicament.name,
                'brand': medicament.name,
                'quantity': medicament.quantity,
                'unit': medicament.unit,
                'ingredients':medicament.ingredients ,
                'contains': medicament.contains,

    }
    with engine.connect() as c:
        try:
            getMedicament(medicament.id)
            return "Cannot create Medicament, already exists"
        except HTTPException as e:
            c.execute(medicaments.insert().values(medicamentd))
            c.commit()
            return medicamentd
        


@app.post("/ips/{id_ips}/medicaments")
def addMedicamentIPS( mavaliable: Medicament_avaliable ,id_ips: int = Path(..., title="ID of the IPS in the URL")):
    medicamentd = { 
        'id_ips': id_ips,
        'id_medicament': mavaliable.id_medicament,
        'avaliable': mavaliable.avaliable, 
        'price': mavaliable.price
    }
    with engine.connect() as c:
        try:
            getMedAvaliability(id_ips, mavaliable.id_medicament)
            return "Cannot create Medicament, already exists"
        except HTTPException :
            try:
                getMedicament(mavaliable.id_medicament)
                getIPS(id_ips)
                c.execute(med_avaliability.insert().values(medicamentd))
                c.commit()
                return medicamentd
            except Exception :
                return HTTPException(status_code=404, detail="IPS or Medicament does not exists.")




@app.post("/doctors")
def addDoctor(doctor: Doctor ):
    doctord = { 
                'id': doctor.id,
                'name': doctor.name,
                'birth': doctor.birth,
                'gender': doctor.gender,
                'pnumber': doctor.pnumber, 
                'email': doctor.email
    }
    with engine.connect() as c:    
        try:
            getDoctor(doctor.id)
            return "Cannot create Docttor, already exists"
        except HTTPException as e:
            c.execute(doctors.insert().values(doctord))
            c.commit()
            return doctord

@app.post("/services")
def addService(service: Service ):
    serviced = { 
                'id': service.id,
                'speciality': service.speciality
    }
    with engine.connect() as c:    
        try:
            getService(service.id)
            return "Cannot create Service, already exists"
        except HTTPException as e:
            try:
                c.execute(services.insert().values(serviced))
                c.commit()
                return serviced
            except Exception as e:
                return "Service already exists"


@app.post("/appointments")
def addAppointment(appointment: Appointment ):
    appointmentd = { 
                'id': appointment.id,
                'date': appointment.date,
                'time': appointment.time,
                'duration': appointment.duration,
                'address': appointment.address,
                'patient_id' : appointment.patient_id,
                'doctor_id' : appointment.doctor_id,
                'service_id' : appointment.service_id
    }
    with engine.connect() as c:     
        try:
            getAppointment(appointment.id)
            getDoctor(appointment.doctor_id)
            getPatient(appointment.patient_id)
            getService(appointment.service_id)
            return "Cannot create appointment"
        except HTTPException as e:
    
            c.execute(appointments.insert().values(appointmentd))
            c.commit()
            return appointmentd 


#UPDATE 
@app.put("/patients/{id}")
def updatePatient(id: int, patient: Patient):
    patientd = {
        'name': patient.name,
        'birth': patient.birth,
        'gender': patient.gender,
        'pnumber': patient.pnumber,
        'email': patient.email
    }
    with engine.connect() as c:
        try:
            getPatient(id)
            c.execute(patients.update().where(patients.c.id == id).values(**patientd))
            c.commit()
            return patientd
        except HTTPException as e:
            return "Patient does not exist"

@app.put("/doctors/{id}")
def updateDoctor(id: int, doctor: Doctor):
    doctord = {
        'name': doctor.name,
        'birth': doctor.birth,
        'gender': doctor.gender,
        'pnumber': doctor.pnumber,
        'email': doctor.email
    }
    with engine.connect() as c:
        try:
            getDoctor(id)
            c.execute(doctors.update().where(doctors.c.id == id).values(**doctord))
            c.commit()
            return doctord
        except HTTPException as e:
            return "Doctor does not exist"
        
@app.put("/services/{id}")
def updateService(id: int, service: Service):
    serviced = {
        'speciality': service.speciality
    }
    with engine.connect() as c:
        try:
            getService(id)
            c.execute(services.update().where(services.c.id == id).values(**serviced))
            c.commit()
            return serviced
        except HTTPException as e:
            return "Service does not exist"

@app.put("/appointments/{id}")
def updateAppointment(id: int, appointment: Appointment):
    appointmentd = {
        'date': appointment.date,
        'time': appointment.time,
        'duration': appointment.duration,
        'address': appointment.address,
        'patient_id': appointment.patient_id,
        'doctor_id': appointment.doctor_id,
        'service_id': appointment.service_id
    }
    with engine.connect() as c:
        try:
            getAppointment(id)
            c.execute(appointments.update().where(appointments.c.id == id).values(**appointmentd))
            c.commit()
            return appointmentd
        except HTTPException as e:
            return "Appointment does not exist"
#DELETE

@app.delete("/patients/{id}")
def deletePatient(id: int):
    with engine.connect() as c:
        stmt = patients.delete().where(patients.c.id == id)
        result = c.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        c.commit()
        return {"message": "Patient deleted successfully"}


@app.delete("/doctors/{id}")
def deleteDoctor(id: int):
    with engine.connect() as c:
        stmt = doctors.delete().where(doctors.c.id == id)
        result = c.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Doctor not found")
        c.commit()
        return {"message": "Doctor deleted successfully"}


@app.delete("/appointments/{id}")
def deleteAppointment(id: int):
    with engine.connect() as c:

        stmt = appointments.delete().where(appointments.c.id == id)
        result = c.execute(stmt)
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Appointment not found")
        c.commit()
        return {"message": "Appointment deleted successfully"}
    

@app.delete("/services/{id}")
def deleteService(id: int):
    with engine.connect() as c:

        stmt = services.delete().where(services.c.id == id)
        result = c.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Service not found")
        c.commit()
        return {"message": "Service deleted successfully"}

@app.get("/") 
def root():
    with engine.connect() as c:
        postgresql_version = c.execute(text("SELECT version()")).fetchone()[0]
        return ["Hello world", {"postgres_version": postgresql_version}]
    
