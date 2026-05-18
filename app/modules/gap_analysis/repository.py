from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.gap_analysis.models import GapAnalysis


def save(db: Session, gap_analysis: GapAnalysis) -> GapAnalysis:
    db.add(gap_analysis)
    db.commit()
    db.refresh(gap_analysis)
    return gap_analysis


def find_by_id(db: Session, gap_id: int) -> GapAnalysis | None:
    return db.get(GapAnalysis, gap_id)


def find_by_student(
    db: Session, student_email: str, offset: int = 0, limit: int = 100
) -> list[GapAnalysis]:
    statement = (
        select(GapAnalysis)
        .where(func.lower(GapAnalysis.student_email) == student_email.lower())
        .order_by(GapAnalysis.id.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement).all())
