from sqlalchemy import (
    Table,
    Integer,
    Column,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from .base import metadata
import datetime

responds = Table(
    "responds",
    metadata,
    Column("id", Integer, autoincrement=True, unique=True),
    Column("job_id", Integer, ForeignKey('jobs.id'),
           primary_key=True, nullable=False),
    Column("user_id", Integer, ForeignKey('users.id'),
           primary_key=True, nullable=False),
    Column("created_at", DateTime, default=datetime.datetime.utcnow()),
    UniqueConstraint('job_id', 'user_id', name='unique_user_job_respond')
)
