from app.database.database import engine, Base

from app.models import job
from app.models import profile


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created!")