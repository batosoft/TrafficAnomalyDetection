from database import Base, engine
from models import User, Anomaly, AnomalyAction, AuditLog

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()