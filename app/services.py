from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models


# -------------------------
# DOCTOR SERVICES
# -------------------------

def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(
        models.Doctor.id == doctor_id
    ).first()


def get_doctors(
    db: Session,
    specialization=None,
    is_active=None,
    skip=0,
    limit=10
):
    query = db.query(models.Doctor)

    if specialization:
        query = query.filter(
            models.Doctor.specialization == specialization
        )

    if is_active is not None:
        query = query.filter(
            models.Doctor.is_active == is_active
        )

    total = query.count()

    doctors = query.offset(skip).limit(limit).all()

    return doctors, total


def create_doctor(db: Session, doctor_data):
    existing_doctor = db.query(models.Doctor).filter(
        models.Doctor.email == doctor_data.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    doctor = models.Doctor(
        name=doctor_data.name,
        email=doctor_data.email,
        phone=doctor_data.phone,
        specialization=doctor_data.specialization,
        is_active=True
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


def update_doctor(
    db: Session,
    doctor_id: int,
    doctor_data,
    partial=False
):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    data = doctor_data.model_dump(exclude_unset=partial)

    if "email" in data:
        existing = db.query(models.Doctor).filter(
            models.Doctor.email == data["email"],
            models.Doctor.id != doctor_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Doctor email already exists"
            )

    for key, value in data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor


def delete_doctor(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False

    db.commit()
    db.refresh(doctor)

    return doctor


# -------------------------
# PATIENT SERVICES
# -------------------------

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()


def get_patients(
    db: Session,
    age_gt=None,
    skip=0,
    limit=10
):
    query = db.query(models.Patient)

    if age_gt is not None:
        query = query.filter(
            models.Patient.age > age_gt
        )

    total = query.count()

    patients = query.offset(skip).limit(limit).all()

    return patients, total


def create_patient(db: Session, patient_data):
    doctor = get_doctor(db, patient_data.doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign patient to inactive doctor"
        )

    patient = models.Patient(
        name=patient_data.name,
        age=patient_data.age,
        phone=patient_data.phone,
        doctor_id=patient_data.doctor_id
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def update_patient(
    db: Session,
    patient_id: int,
    patient_data,
    partial=False
):
    patient = get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    data = patient_data.model_dump(exclude_unset=partial)

    if "doctor_id" in data:
        doctor = get_doctor(db, data["doctor_id"])

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if not doctor.is_active:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign patient to inactive doctor"
            )

    for key, value in data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient


def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {"message": "Patient deleted successfully"}


def get_doctor_patients(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Doctor is inactive"
        )

    return db.query(models.Patient).filter(
        models.Patient.doctor_id == doctor_id
    ).all()