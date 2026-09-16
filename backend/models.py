from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func

from backend.database import Base


class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)

    constituency = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    risk_score = Column(Float, nullable=False)
    risk_category = Column(String, nullable=False)

    status = Column(
        String,
        default="Under Review",
        nullable=False
    )

    officer_remarks = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )