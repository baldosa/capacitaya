from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GapAnalysis(Base):
    __tablename__ = "gap_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    company_email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    readiness_score: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    gap_report_json: Mapped[str] = mapped_column(Text, nullable=False)
    student_doc_text: Mapped[str] = mapped_column(Text, nullable=False)
    position_doc_text: Mapped[str] = mapped_column(Text, nullable=False)
    learning_path_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    generator_used: Mapped[str] = mapped_column(
        String(20), nullable=False, default="groq"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
