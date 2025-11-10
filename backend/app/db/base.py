from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


def normalize_db_url(db_url: str) -> str:
    """Normalize DB URL for Render / PostgreSQL compatibility."""
    # Convert old-style prefix
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # Add sslmode=require if not present (Render requires SSL)
    parsed = urlparse(db_url)
    query = dict(parse_qsl(parsed.query))
    if "sslmode" not in query:
        query["sslmode"] = "require"

    new_query = urlencode(query)
    db_url = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment)
    )
    return db_url


# Normalize the URL
db_url = normalize_db_url(settings.DATABASE_URL)

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create the engine
engine = create_engine(db_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    """Initialize database models on startup."""
    from app.db import models  # noqa
    Base.metadata.create_all(bind=engine)
