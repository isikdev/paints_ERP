"""Insert document types

Revision ID: 6318f8c97929
Revises: 9854de4134de
Create Date: 2025-04-22 10:09:56.127362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import uuid
from sqlalchemy.dialects.postgresql import UUID

from constants import MAX_NAME_LENGTH, DocumentTypes


revision: str = '2'
down_revision: Union[str, None] = '1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    document_types_table = sa.table(
        'document_types',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('name', sa.String(MAX_NAME_LENGTH)),
        sa.Column('direction', sa.Integer(), nullable=False),
    )
    document_types = [
        {'id': uuid.uuid4(), 'name': dt['name'], 'direction': dt['direction']}
        for dt in DocumentTypes
    ]
    op.bulk_insert(document_types_table, document_types)


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()
    document_types_table = sa.table(
        'document_types',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('name', sa.String(MAX_NAME_LENGTH)),
    )
    names = [dt['name'] for dt in DocumentTypes]
    connection.execute(
        sa.text("DELETE FROM document_types WHERE name IN :names"),
        {"names": names}
    )
