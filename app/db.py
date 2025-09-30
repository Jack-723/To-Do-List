from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "todo.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Needed for SQLite + FastAPI in dev
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
