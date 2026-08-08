from Projects.foothold.app.database.database import Base, engine
from app.models.job import Job
from app.models.profile import Profile


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created!")