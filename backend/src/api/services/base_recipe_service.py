import json

from constants import RULES_EXAMPLE, DocumentTypesEnum
from api.schemas import BaseRecipeCreateRequest

if __name__ == '__main__':
    # base_recipe = BaseRecipeCreateRequest(
    #     rules=RULES_EXAMPLE,
    # )
    # print(base_recipe.model_dump())
    print(DocumentTypesEnum.BaseRecipeType.name)
    # base_recipe.rules.pigment_part[0].materials[0].items
    # from copy import deepcopy
    # rules = deepcopy(VALID_RULES)
    # empty_materials_rules = deepcopy(rules)
    # empty_materials_rules['film_former_part']['materials'] = []
    # # print(base_recipe.rules)
    # print(json.dumps(empty_materials_rules))