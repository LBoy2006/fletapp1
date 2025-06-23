import os
import sys
from logging.config import fileConfig

from alembic import context

# Добавляем путь к backend, чтобы видеть models и database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend import models
from backend.database import DATABASE_URL

# Получаем Alembic Config
config = context.config

# Настройка логирования (опционально, но лучше оставить)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# СИНХРОНИЗИРУЕМ URL для alembic
sync_url = DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite:///") \
                       .replace("postgresql+asyncpg://", "postgresql+psycopg2://")

# Переопределяем URL для Alembic (ОБЯЗАТЕЛЬНО до создания engine!)
config.set_main_option("sqlalchemy.url", sync_url)

# Для дебага — проверяем, какой URL реально подставлен
print("FROM ENV:", os.environ.get("DATABASE_URL"))
print("FROM settings:", DATABASE_URL)
print("sync_url:", sync_url)
print("ALEMBIC URL:", config.get_main_option("sqlalchemy.url"))

# MetaData моделей (нужно для автогенерации миграций)
target_metadata = models.Base.metadata

from sqlalchemy import engine_from_config, pool

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
