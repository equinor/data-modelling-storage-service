from alembic import context
from sqlalchemy import create_engine
import os
import sys
from sqlalchemy.types import TypeDecorator, CHAR
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from storage.repositories.plugin.sql.config import Config
from storage.repositories.plugin.sql.models import Base

class UUID(TypeDecorator):
    """Platform-independent UUID type."""
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(CHAR(32))
        else:
            return dialect.type_descriptor(PG_UUID())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'sqlite':
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int
        else:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def get_url():
    """Return the database URL"""
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        return Config().SQLALCHEMY_DATABASE_URI
    return url

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and reflected:
        return False
    elif type_ == 'foreign_key_constraint' and reflected:
        return False
    elif name and 'id' in name and reflected:
        return False
    else:
        return True

def my_render_column(type_, col, autogen_context):
    if type_ == "primary_key":
        for i in col.columns:
            if 'skip_pk' in i.info and i.info['skip_pk']:
                return None
        return False
    else:
        return False

def run_migrations_offline():
    url = get_url()
    context.configure(
        compare_type=True,
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        include_object=include_object,
        render_item=my_render_column
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url())

    def process_revision_directives(context, revision, directives):
        if not directives[0].upgrade_ops.ops:
            directives[:] = []
            print('No changes in schema detected.')

    with connectable.connect() as connection:
        context.configure(
            compare_type=True,
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
            render_item=my_render_column
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()