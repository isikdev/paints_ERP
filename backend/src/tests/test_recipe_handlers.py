from copy import deepcopy
from fastapi.encoders import jsonable_encoder
import uuid
import pytest

from constants import RULES_EXAMPLE

class TestRecipeHandlers:

    @pytest.mark.usefixtures('get_data_for_recipe')
    async def test_create_recipe(self, client, get_data_for_recipe):
        response = await client.post(f'/api/v1/document/type/?name=Base Recipe')
        assert response.status_code == 200

        rules = deepcopy(RULES_EXAMPLE)
        body = {
            "document_datetime": "2025-04-19 16:00:00",
            "commentary": "Comment for Base Recipe",
            'rules': rules,
            'status': 'Posted',
            'name': 'ПФ-115'
        }

        response = await client.post("/api/v1/document/base-recipe/", json=jsonable_encoder(body))
        assert response.status_code == 200
        base_recipe_id = response.json()['id']

        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'base_recipe_id': base_recipe_id,
            'nomenclature_id': get_data_for_recipe['paint_id'],
            'batch_amount': 1000
        }

        assert isinstance(get_data_for_recipe['paint_id'], uuid.UUID)
        response = await client.post("/api/v1/document/recipe/", json=jsonable_encoder(body))
        assert response.status_code == 200

        # assert response.status_code == 200
        # result = response.json()
        # base_recipe_id = result['id']

