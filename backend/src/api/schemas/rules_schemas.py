import uuid
from typing import (
    Annotated,
    TypeAlias,
    Self
)

from pydantic import (
    conlist,
    Field,
    model_validator,
    PositiveFloat,
    PositiveInt,
    RootModel,
    field_validator
)

from .base_models import BaseModel
from constants import DosageTypeEnum

UUIDList = Annotated[
    conlist(uuid.UUID | None, min_length=1),
    Field(description="List of UUIDs")
]
RatioList = Annotated[conlist(PositiveInt | None, min_length=1), Field(description="List of positive integers")]

class MaterialDict(BaseModel):
    uuids: UUIDList
    ratios: RatioList
    dosage: dict[DosageTypeEnum, PositiveFloat | None] | None = None

    @field_validator('dosage')
    def exactly_one_method(cls, v: dict[DosageTypeEnum, PositiveFloat] | None):
        if v:
            if len(v.keys()) != 1:
                raise ValueError(
                    f'Field dosage must contain only one dosage method {list(DosageTypeEnum)}'
                )
        return v


class MaterialList(RootModel[list[MaterialDict]]):
    """List of pairs (material_ids, quantities)."""
    root: list[MaterialDict]

    @model_validator(mode='after')
    def validate_materials(self) -> Self:
        for m_dict in self.root:
            if len(m_dict.uuids) != len(m_dict.ratios):
                raise ValueError(
                    f"Length of list of raw_materials = {len(m_dict['uuids'])} "
                    f"and ratios = {len(m_dict.ratios)} and should be equal"
                )
            if len(m_dict.uuids) == 1 and m_dict.ratios[0] != 1:
                raise ValueError(
                    "if only one material entry is provided, the ratio must be equal to 1."
                )
        return self


class Materials(BaseModel):
    """Scheme describing list of raw materials with ratios."""
    materials: MaterialList


NomenclatureGroupID = Annotated[
    uuid.UUID | None,
    Field(description='Nomenclature type name with max length 100 symbols.')
]


class CategorisedMaterials(BaseModel):
    """Scheme describing a category with corresponding list of raw materials."""
    nomenclature_group_id: NomenclatureGroupID
    items: MaterialList


CategorisedMaterialsList = Annotated[
    list[CategorisedMaterials],
    Field(description='Categorised material field:.')
]


class CategoryWithMaterials(BaseModel):
    """Scheme describing materials divided by categories."""
    materials: CategorisedMaterialsList


ColorName: TypeAlias = str | None
RuleRatio = Annotated[PositiveFloat | None, Field(description="Ratio")]


class ColoredMaterials(BaseModel):
    """Scheme describing rules that is affected by color."""
    color: ColorName
    materials: CategorisedMaterialsList
    dry_residue: RuleRatio
    pigmentation_degree: RuleRatio
    filler_ratio: RuleRatio


PigmentPart: TypeAlias = list[ColoredMaterials]


class Rules(BaseModel):
    """Scheme describing JSON containing rules for base recipe."""
    film_former_part: Materials
    pigment_part: PigmentPart
    additives_part: CategoryWithMaterials
    solvent_part: Materials
    is_posted: bool = False

    @staticmethod
    def check_material_list(material_list: MaterialList, path: str) -> None:
        if not material_list.root:
            raise ValueError("Materials list must not be empty")
        for i, item in enumerate(material_list.root):
            if None in item.uuids:
                raise ValueError(f'Set value of nomenclature id in {path}.root[{i}].uuids')
            if None in item.ratios:
                raise ValueError(f'Set value of material ratio in {path}.root[{i}].ratios')
            if item.dosage is not None:
                if None in item.dosage.values():
                    raise ValueError(f'If you set dosage_method, provide value.')

    @staticmethod
    def validate_nom_groups(cat_list: CategorisedMaterialsList, seen_groups: set, path: str) -> None:
        """Check that materials with categories have unique categories."""
        for i, category in enumerate(cat_list):
            group_id = category.nomenclature_group_id
            if not group_id:
                raise ValueError("Nomenclature group id must be specified for all categories."
                                 f"\n Set value of {path + f'[{i}].nomenclature_group_id.'}")
            if group_id in seen_groups:
                raise ValueError(f'Nomenclature group id already defined within {path}.')
            seen_groups.add(group_id)
            new_path = path + f'[{i}].items'
            Rules.check_material_list(category.items, path=new_path)

    @staticmethod
    def check_categorised_materials_list(cat_list: CategorisedMaterialsList, path: str = None) -> None:
        seen_nomenclature_groups = set()
        Rules.validate_nom_groups(cat_list, seen_nomenclature_groups, path)

    @staticmethod
    def check_has_color_names(colored_materials_dict: ColoredMaterials, dict_number: int, seen_colors: set) -> None:
        if not colored_materials_dict.color:
            raise ValueError(f"Set value of color name in rules.pigment_part[{dict_number}].color.")
        if colored_materials_dict.color in seen_colors:
            raise ValueError(f"Color '{colored_materials_dict.color}' is duplicated")
        seen_colors.add(colored_materials_dict.color)

    @staticmethod
    def check_pigment_part_has_necessary_parameters(colored_materials_dict: ColoredMaterials, dict_number: int) -> None:
        if not colored_materials_dict.materials:
            raise ValueError(f"Materials for color {colored_materials_dict.color} must be specified.")
        if not colored_materials_dict.dry_residue:
            raise ValueError(f"Set value of dry residue amount in rules.pigment_part[{dict_number}].dry_residue.")
        if not colored_materials_dict.pigmentation_degree:
            raise ValueError(
                f"Set value of pigmentation_degree in rules.pigment_part[{dict_number}].pigmentation_degree."
            )
        if not colored_materials_dict.filler_ratio:
            raise ValueError(f"Set value of filler_ratio in rules.pigment_part[{dict_number}].filler_ratio.")

    @staticmethod
    def check_colored_materials(colored_materials_list: PigmentPart, path: str = None) -> None:
        if not colored_materials_list:
            raise ValueError("At least one pigment part with color must be specified.")

        seen_colors = set()
        for i, colored_materials_dict in enumerate(colored_materials_list):
            Rules.check_has_color_names(colored_materials_dict, i, seen_colors)
            Rules.check_pigment_part_has_necessary_parameters(colored_materials_dict, i)
            new_path = path + f'[{i}].materials'
            Rules.check_categorised_materials_list(colored_materials_dict.materials, new_path)

    @model_validator(mode='after')
    def validate_rules_for_posting(self) -> Self:
        if self.is_posted:
            self.check_material_list(self.film_former_part.materials, path="rules.film_former_part.materials")
            self.check_colored_materials(self.pigment_part, path="rules.pigment_part")
            self.check_categorised_materials_list(self.additives_part.materials, path="rules.additives_part.materials")
            self.check_material_list(self.solvent_part.materials, path=f"rules.solvent_part")
        return self
