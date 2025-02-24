from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os

# ✅ 여기에 Base import 추가!
from app.models.base import Base

# 환경 변수에서 DB URL 가져오기
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "postgresql://psql:hateyou417@10.99.222.32:5432/psql"))

# Logging 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Alembic이 DB 스키마를 감지하도록 설정
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
