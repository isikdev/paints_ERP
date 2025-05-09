"""insert data for recipe

Revision ID: 743163bae2b7
Revises: 554137594755
Create Date: 2025-04-23 09:22:28.341021

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder

import json

from constants import BASE_RECIPE_BODY_EXAMPLE, STANDARD_NOMENCLATURE_TYPES, STANDARD_NOMENCLATURE_GROUPS, STANDARD_MEASURE_UNITS, NOMENCLATURES, RULES_EXAMPLE, DocumentTypesEnum


revision: str = '6'
down_revision: Union[str, None] = '5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    mu_table = sa.table(
        "measure_units",
        sa.column("id", sa.UUID(as_uuid=True)),
        sa.column("name", sa.String),
        sa.column("short_name", sa.String),
    )
    op.bulk_insert(mu_table, STANDARD_MEASURE_UNITS)

    # nomenclature_types
    nt_table = sa.table(
        "nomenclature_types",
        sa.column("id", sa.UUID(as_uuid=True)),
        sa.column("name", sa.String),
    )
    op.bulk_insert(nt_table, STANDARD_NOMENCLATURE_TYPES)

    # nomenclature_groups
    ng_table = sa.table(
        "nomenclature_groups",
        sa.column("id", sa.UUID(as_uuid=True)),
        sa.column("parent_id", sa.UUID(as_uuid=True)),
        sa.column("name", sa.String(100)),
    )
    op.bulk_insert(ng_table, STANDARD_NOMENCLATURE_GROUPS)

    # nomenclatures
    nom_table = sa.table(
        "nomenclatures",
        sa.column("id", sa.UUID(as_uuid=True)),
        sa.column("name", sa.String(100)),
        sa.column("description", sa.Text),
        sa.column("type_id", sa.UUID(as_uuid=True)),
        sa.column("group_id", sa.UUID(as_uuid=True)),
        sa.column("measure_unit_id", sa.UUID(as_uuid=True)),
        sa.column("properties", sa.dialects.postgresql.JSONB),
    )
    rows = []
    for rec in NOMENCLATURES:
        rows.append({
            "id": rec["id"],
            "name": rec["name"],
            "description": rec.get("description", ""),
            "type_id": rec["type_id"],
            "group_id": rec["group_id"],
            "measure_unit_id": rec["measure_unit_id"],
            "properties": jsonable_encoder(rec.get("properties", {}))
        })
    op.bulk_insert(nom_table, rows)

    base_recipes_table = sa.table(
        "base_recipes",
        sa.column("id", sa.UUID(as_uuid=True)),
        sa.column("document_number", sa.Integer),
        sa.column("status", sa.String(20)),
        sa.column("document_datetime", sa.DateTime(timezone=True)),
        sa.column("name", sa.String(100)),
        sa.column("commentary", sa.Text),
        sa.column("document_type_id", sa.UUID(as_uuid=True)),
        sa.column("rules", sa.dialects.postgresql.JSONB),
    )
    assoc_table = sa.table(
        "nomenclature_base_recipe_association",
        sa.column("base_recipe_id", sa.UUID(as_uuid=True)),
        sa.column("nomenclature_id", sa.UUID(as_uuid=True)),
    )

    document_types_table = sa.table(
        'document_types',
        sa.column('id', sa.UUID(as_uuid=True)),
        sa.column('name', sa.String(100)),
    )
    connection = op.get_bind()
    document_type_id = connection.execute(
        sa.select(document_types_table.c.id)
        .where(document_types_table.c.name == DocumentTypesEnum.BaseRecipeType.value)
    ).scalar_one()
    new_id = uuid.uuid4()
    body = BASE_RECIPE_BODY_EXAMPLE.copy()
    connection.execute(
        base_recipes_table.insert().values(
            id=new_id,
            document_number=None,
            status=body["status"],
            document_datetime=body["document_datetime"],
            name=body["name"],
            commentary=body.get("commentary"),
            document_type_id=document_type_id,
            rules=jsonable_encoder(body["rules"]),
        )
    )

    connection.execute(
        assoc_table.insert().values(
            base_recipe_id=new_id,
            nomenclature_id=NOMENCLATURES[0]['id'],

        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    conn.execute("DELETE FROM base_recipes WHERE document_number = 1")

    names = tuple(r["name"] for r in NOMENCLATURES)
    conn.execute(
        sa.text("DELETE FROM nomenclatures WHERE name IN :names"),
        {"names": names}
    )
    # delete groups
    gnames = tuple(g["name"] for g in STANDARD_NOMENCLATURE_GROUPS)
    conn.execute(
        sa.text("DELETE FROM nomenclature_groups WHERE name IN :names"),
        {"names": gnames}
    )
    # delete types
    tnames = tuple(t["name"] for t in STANDARD_NOMENCLATURE_TYPES)
    conn.execute(
        sa.text("DELETE FROM nomenclature_types WHERE name IN :names"),
        {"names": tnames}
    )
    # delete units
    unames = tuple(u["name"] for u in STANDARD_MEASURE_UNITS)
    conn.execute(
        sa.text("DELETE FROM measure_units WHERE name IN :names"),
        {"names": unames}
    )
