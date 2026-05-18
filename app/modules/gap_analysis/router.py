from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.gap_analysis import service
from app.modules.gap_analysis.schemas import (
    GapAnalysisResponse,
    GapAnalysisWithPlanResponse,
)
from app.modules.learning_paths.plan_generator.base import PlanGenerator
from app.modules.learning_paths.plan_generator.factory import get_plan_generator
from app.modules.learning_paths.repository.base import LearningPathRepository
from app.modules.learning_paths.repository.factory import get_learning_path_repository


router = APIRouter(prefix="/gap-analyses", tags=["gap-analyses"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GapAnalysisResponse,
)
def create_gap_analysis(
    student_email: str = Form(...),
    company_email: str = Form(...),
    student_doc: UploadFile = File(...),
    position_doc: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> GapAnalysisResponse:
    return service.create_gap_analysis(
        db=db,
        student_email=student_email,
        company_email=company_email,
        student_doc=student_doc,
        position_doc=position_doc,
    )


@router.get("/{gap_id}", response_model=GapAnalysisResponse)
def get_gap_analysis(
    gap_id: int, db: Session = Depends(get_db)
) -> GapAnalysisResponse:
    return service.get_gap_analysis(db, gap_id)


student_gap_analyses_router = APIRouter(prefix="/students", tags=["gap-analyses"])


@student_gap_analyses_router.get(
    "/{email}/gap-analyses", response_model=list[GapAnalysisResponse]
)
def list_by_student(
    email: str,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[GapAnalysisResponse]:
    return service.list_by_student(db, email, offset=offset, limit=limit)


@student_gap_analyses_router.post(
    "/{email}/generate-learning-path",
    status_code=status.HTTP_201_CREATED,
    response_model=GapAnalysisWithPlanResponse,
)
def generate_learning_path_for_student(
    email: str,
    db: Session = Depends(get_db),
    plan_generator: PlanGenerator = Depends(get_plan_generator),
    lp_repository: LearningPathRepository = Depends(get_learning_path_repository),
) -> GapAnalysisWithPlanResponse:
    return service.generate_learning_path_for_student(
        db=db,
        student_email=email,
        plan_generator=plan_generator,
        lp_repository=lp_repository,
    )
