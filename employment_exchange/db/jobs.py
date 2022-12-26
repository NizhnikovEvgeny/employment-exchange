from sqlalchemy import (
    Table,
    Integer,
    String,
    Column,
    Boolean,
    DateTime,
    ForeignKey
)
from .base import metadata
import datetime

jobs = Table(
    "jobs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("user_id", Integer, ForeignKey('users.id'), nullable=False),
    Column("title", String),
    Column("salary_from", Integer),
    Column("salary_to", Integer),
    Column("is_active", Boolean, default=False),
    Column("created_at", DateTime, default=datetime.datetime.utcnow()),
    Column("updated_at", DateTime, default=datetime.datetime.utcnow()),
)
