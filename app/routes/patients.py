from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, services
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post(
    "/",
    response_model=schemas.PatientResponse,
    status_code=201
)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db)
):
    return services.create_patient(
        db,
        patient
    )
@router.post(
    "/",
    response_model=schemas.PatientResponse,
    status_code=201
)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return services.create_patient(
        db,
        patient
    )
@router.get(
    "/",
    response_model=schemas.PatientPaginationResponse
)
def get_patients(
    age_gt: int | None = Query(None, gt=0),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    patients, total = services.get_patients(
        db,
        age_gt,
        skip,
        limit
    )

    return {
        "total": total,
        "current_page": page,
        "limit": limit,
        "data": patients
    }




@router.get(
    "/{patient_id}",
    response_model=schemas.PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    from fastapi import HTTPException

    patient = services.get_patient(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@router.put(
    "/{patient_id}",
    response_model=schemas.PatientResponse
)
def update_patient(
    patient_id: int,
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)

):
    return services.update_patient(
        db,
        patient_id,
        patient,
        partial=False
    )


@router.patch(
    "/{patient_id}",
    response_model=schemas.PatientResponse
)
def partial_update_patient(
    patient_id: int,
    patient: schemas.PatientUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)

):
    return services.update_patient(
        db,
        patient_id,
        patient,
        partial=True
    )


@router.delete(
    "/{patient_id}"
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)

):
    return services.delete_patient(
        db,
        patient_id
    )