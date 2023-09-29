from pydantic import BaseModel, ConfigDict
from datetime import time, date

# Schemas

class Patient(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    birth: str
    gender: str
    pnumber:int
    email:str
class Doctor(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    birth: str
    gender: str
    pnumber:int
    email:str
class Schedule(BaseModel):
    id: int
    startday: str
    endday: str
    starttime: time 
    endtime: time

class Appointment(BaseModel):
    id: int
    date: date
    time: time
    duration: int
    address:str
    patient_id: int
    doctor_id: int
    service_id: int
class Service(BaseModel):
    id: int
    speciality: str


class IPS(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    pnumber:int
    email:str
    address:str

class EPS(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    pnumber:int
    email:str
    address:str

class Admin(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    pnumber:int
    email:str
    permissions:int

class Medicament(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    brand: str
    quantity: float
    unit : int
    ingredients : str
    contains: int
    
class Medicament_avaliable(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id_ips: int
    id_medicament: int
    avaliable: int
    price: float

class MedicamentDetail(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    brand: str
    quantity: float
    unit : int
    ingredients : str
    contains: int
    avaliable: int
    price: float