# backend/init_db.py
from backend.database import engine, Base
from backend.database.users import UserModel
from backend.database.articles import ArticleModel
from backend.database.research_notes import ResearchNoteModel

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()