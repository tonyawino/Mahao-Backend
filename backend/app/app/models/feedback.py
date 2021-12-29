from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Feedback(Base):
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("property.id"), index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    feedback_type = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    property = relationship("Property", back_populates="feedbacks")
    user = relationship("User", back_populates="feedbacks")
