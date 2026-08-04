from sqlalchemy import Column, Integer, String, Boolean, Text

from app.database.database import Base


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    target_titles = Column(Text, nullable=True)

    minimum_salary = Column(Integer, nullable=True)

    remote_only = Column(Boolean, default=True)

    skills = Column(Text, nullable=True)

    certifications = Column(Text, nullable=True)

    preferred_industries = Column(Text, nullable=True)

    avoid_keywords = Column(Text, nullable=True)