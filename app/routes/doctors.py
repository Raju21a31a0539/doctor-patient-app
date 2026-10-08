from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, services
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post(
    "/",
    response_model=schemas.DoctorResponse,
    status_code=201
)
def create_doctor(
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return services.create_doctor(
        db,
        doctor
    )

@router.get(
    "/",
    response_model=schemas.DoctorPaginationResponse
)
def get_doctors(
    specialization: str | None = Query(None),
    is_active: bool | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    doctors, total = services.get_doctors(
        db,
        specialization,
        is_active,
        skip,
        limit
    )

    return {
        "total": total,
        "current_page": page,
        "limit": limit,
        "data": doctors
    }

# @router.get(
#     "/",
#     response_model=list[schemas.DoctorResponse]
# )
# def get_doctors(
#     specialization: str | None = Query(None),
#     is_active: bool | None = Query(None),
#     page: int = Query(1, ge=1),
#     limit: int = Query(10, ge=1, le=100),
#     db: Session = Depends(get_db)
# ):
#     skip = (page - 1) * limit

#     doctors, total = services.get_doctors(
#         db,
#         specialization,
#         is_active,
#         skip,
#         limit
#     )

#     return doctors


@router.get(
    "/{doctor_id}",
    response_model=schemas.DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = services.get_doctor(db, doctor_id)

    if not doctor:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.get(
    "/{doctor_id}/patients",
    response_model=list[schemas.PatientResponse]
)
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    return services.get_doctor_patients(
        db,
        doctor_id
    )

@router.put(
    "/{doctor_id}",
    response_model=schemas.DoctorResponse
)
def update_doctor(
    doctor_id: int,
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return services.update_doctor(
        db,
        doctor_id,
        doctor,
        partial=False
    )

@router.patch(
    "/{doctor_id}",
    response_model=schemas.DoctorResponse
)
def partial_update_doctor(
    doctor_id: int,
    doctor: schemas.DoctorUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return services.update_doctor(
        db,
        doctor_id,
        doctor,
        partial=True
    )

@router.delete(
    "/{doctor_id}"
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    services.delete_doctor(
        db,
        doctor_id
    )

    return {
        "message": "Doctor deactivated successfully"
    }