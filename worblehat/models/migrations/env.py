from alembic import context
from flask import current_app
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from worblehat.models import Base
from worblehat.services.config import Config

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

Config.load_configuration({})

config.set_main_option('sqlalchemy.url', Config.db_string())

# This will make sure alembic doesn't generate empty migrations
# https://stackoverflow.com/questions/70203927/how-to-prevent-alembic-revision-autogenerate-from-making-revision-file-if-it-h
def _process_revision_directives(context, revision, directives):
    if config.cmd_opts.autogenerate:
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print('No changes in schema detected. Not generating migration.')

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,

            # Extended type checking with alembic when generating migrations
            # https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect
            compare_type=True,

            # This is required for ALTER TABLE to work with sqlite.
            # It should have no effect on postgreSQL
            # https://alembic.sqlalchemy.org/en/latest/batch.html
            render_as_batch=True,
            process_revision_directives=_process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()

# We don't have any good reasons to generate raw sql migrations,
# so the `run_migrations_offline` has been removed
run_migrations_online()
