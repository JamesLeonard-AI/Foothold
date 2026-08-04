from app.database.database import Base, engine
from app.models.job import Job
from app.models.profile import Profile


def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")


if __name__ == "__main__":
    create_tables()