from fastapi.encoders import jsonable_encoder

from api.schemas import BaseRecipeCreateRequest
from api.schemas.rules_schemas import Rules
from db.dals import BaseRecipeDAL
from db.models import BaseRecipe

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import uuid
from db.models import Nomenclature, NomenclatureGroup

class BaseRecipeActions:
    """
    Class containing (along with other helper functions) actions for base recipes,
    i.e. logic of session context managers and DAL calls.
    """
    DAL = BaseRecipeDAL

    @staticmethod
    async def validate_body(body: dict, session: AsyncSession) -> None:
            if not body.get('rules', None):
                raise HTTPException(status_code=422, detail="Rules must be provided for posted documents.")
            body['rules']['is_posted'] = True

            try:
                validated: Rules = Rules.model_validate(body['rules'])
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc))

            nom_ids = set()
            grp_ids = set()

            for mat in validated.film_former_part.materials.root:
                nom_ids.update(mat.uuids)
            color_groups = []
            for colored in validated.pigment_part:
                color_group = set()
                for cat in colored.materials:
                    color_group.add(cat.nomenclature_group_id)
                    grp_ids.add(cat.nomenclature_group_id)
                    for mat in cat.items.root:
                        nom_ids.update(mat.uuids)
                color_groups.append(color_group)

            for cat in validated.additives_part.materials:
                grp_ids.add(cat.nomenclature_group_id)
                for mat in cat.items.root:
                    nom_ids.update(mat.uuids)

            for mat in validated.solvent_part.materials.root:
                nom_ids.update(mat.uuids)

            async with session.begin():
                if nom_ids:
                    rows = await session.execute(
                        select(Nomenclature.id).where(Nomenclature.id.in_(nom_ids))
                    )
                    found = {r[0] for r in rows.fetchall()}
                    missing = nom_ids - found
                    if missing:
                        raise HTTPException(
                            status_code=422,
                            detail=f"Nomenclature id(s) not found: {', '.join(str(m) for m in missing)}"
                        )

                for group in color_groups:
                    row = await session.execute(
                        select(NomenclatureGroup.name)
                        .where(NomenclatureGroup.id.in_(group))
                        .where(NomenclatureGroup.name == 'Пигменты'))
                    found = row.fetchone()

                    if not found:
                        raise HTTPException(
                            status_code=422,
                            detail='There is no group "Пигменты" in pigment part.'
                        )

                    row = await session.execute(
                        select(NomenclatureGroup.name)
                        .where(NomenclatureGroup.id.in_(group))
                        .where(NomenclatureGroup.name == 'Наполнители'))
                    found = row.fetchone()

                    if not found:
                        raise HTTPException(
                            status_code=422,
                            detail='There is no group "Наполнители" in pigment part.'
                        )

                if grp_ids:
                    rows = await session.execute(
                        select(NomenclatureGroup.id).where(NomenclatureGroup.id.in_(grp_ids))
                    )
                    found = {r[0] for r in rows.fetchall()}
                    missing = grp_ids - found
                    if missing:
                        raise HTTPException(
                            status_code=422,
                            detail=f"NomenclatureGroup id(s) not found: {', '.join(str(m) for m in missing)}"
                        )

    @classmethod
    async def create_base_recipe(cls, body: BaseRecipeCreateRequest, session: AsyncSession) -> BaseRecipe:
        async with session.begin():
            base_recipe_dal = cls.DAL(db_session=session)
            body_dump = body.model_dump()
            body_dump["rules"] = jsonable_encoder(body_dump["rules"])
            return await base_recipe_dal.create_base_recipe(**body_dump)

    @classmethod
    async def get_base_recipe(cls, base_recipe_id: uuid.UUID, session: AsyncSession) -> BaseRecipe | None:
        async with session.begin():
            base_recipe_dal = cls.DAL(db_session=session)
            return await base_recipe_dal.get_base_recipe_by_id(id=base_recipe_id)

    @classmethod
    async def get_all_base_recipes(cls, session: AsyncSession) -> list[BaseRecipe] | None:
        async with session.begin():
            base_recipe_dal = cls.DAL(db_session=session)
            return await base_recipe_dal.get_all_base_recipes()

    @classmethod
    async def update_base_recipe(cls, base_recipe_id: uuid.UUID, updates: dict, session: AsyncSession ) -> BaseRecipe:
        async with session.begin():
            base_recipe_dal = cls.DAL(db_session=session)
            if updates.get('rules'):
                updates["rules"] = jsonable_encoder(updates["rules"])
            return await base_recipe_dal.update_base_recipe(base_recipe_id, **updates)

    @classmethod
    async def delete_base_recipe(cls, base_recipe_id: uuid.UUID, session: AsyncSession):
        async with session.begin():
            base_recipe_dal = cls.DAL(db_session=session)
            return await base_recipe_dal.delete_base_recipe(id=base_recipe_id)
