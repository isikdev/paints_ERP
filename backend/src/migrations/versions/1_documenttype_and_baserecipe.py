"""DocumentType and BaseRecipe

Revision ID: 9b504bd55bdb
Revises: 
Create Date: 2025-04-21 17:39:05.230089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_types',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('direction', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_document_types')),
    sa.UniqueConstraint('name', name=op.f('uq_document_types_name'))
    )
    op.create_table('base_recipes',
    sa.Column('rules', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('document_number', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('document_datetime', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('commentary', sa.String(), server_default=sa.text("''"), nullable=False),
    sa.Column('document_type_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['document_type_id'], ['document_types.id'], name=op.f('fk_base_recipes_document_type_id_document_types'), ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_base_recipes')),
    sa.UniqueConstraint('name', 'document_number', name='_unique_name_number_uc')
    )
    op.create_table('document_number_counters',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('document_type_id', sa.UUID(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('counter', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['document_type_id'], ['document_types.id'], name=op.f('fk_document_number_counters_document_type_id_document_types'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_document_number_counters')),
    sa.UniqueConstraint('document_type_id', 'year', name='_unique_document_type_year_uc')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_number_counters')
    op.drop_table('base_recipes')
    op.drop_table('document_types')
    # ### end Alembic commands ###
