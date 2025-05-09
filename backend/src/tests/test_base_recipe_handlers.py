from copy import deepcopy

from constants import RULES_EXAMPLE

import uuid
import json
from httpx import AsyncClient


class TestBaseRecipeHandlers:
    async def test_get_all_recipes_none(self, client: AsyncClient):
        response = await client.get("/api/v1/document/base-recipes/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_base_recipe_success_posted(self, client: AsyncClient):
        type_name = 'Base Recipe'
        type_response = await client.post(f"api/v1/document/type/?name={type_name}")
        assert type_response.status_code == 200
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'rules': rules,
            'status': 'Posted',
            'name': 'ПФ-115'
        }

        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 200
        result = new_response.json()
        base_recipe_id = result['id']
        assert result['document_datetime'] == "2025-04-19T17:00:00Z"
        assert result['name'] == "ПФ-115"
        assert result['status'] == "Posted"
        assert result['commentary'] == "Comment for Base Recipe"
        rules['is_posted'] = True
        assert result['rules'] == assert_rules


        response = await client.get(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}', )
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == base_recipe_id
        assert result['document_datetime'] == "2025-04-19T17:00:00Z"
        assert result['name'] == "ПФ-115"
        assert result['status'] == "Posted"
        assert result['commentary'] == "Comment for Base Recipe"

        assert result['rules'] == assert_rules

    async def test_create_base_recipe_success_registered(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'rules': rules,
            'status': 'Registered',
            'name': 'ПФ-115'
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 200

        base_recipe_id = new_response.json()['id']
        response = await client.get(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}', )
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == base_recipe_id
        assert result['document_datetime'] == "2025-04-19T17:00:00Z"
        assert result['name'] == "ПФ-115"
        assert result['status'] == "Registered"
        assert result['commentary'] == "Comment for Base Recipe"
        assert result['rules'] == assert_rules

    async def test_create_base_recipe_empty_body(self, client: AsyncClient):
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps({}))
        assert new_response.status_code == 200
        base_recipe_id = new_response.json()['id']
        response = await client.get(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}', )
        assert response.status_code == 200
        result = response.json()
        assert result['id']
        assert result['document_datetime']
        assert result['name'] == f"base_recipe_{result['document_number']:03d}_{result['document_datetime'][:4]}"
        assert result['status'] == "Registered"
        assert result['commentary'] == ""
        assert result['rules'] == {}

    async def test_create_base_recipe_success_no_commentary(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            'rules': rules,
            'status': 'Registered',
            'name': 'ПФ-115'
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 200

        base_recipe_id = new_response.json()['id']
        response = await client.get(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}', )
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == base_recipe_id
        assert result['document_datetime'] == "2025-04-19T17:00:00Z"
        assert result['name'] == "ПФ-115"
        assert result['status'] == "Registered"
        assert result['commentary'] == ""
        assert result['rules'] == assert_rules

    async def test_create_base_recipe_success_no_rules(self, client: AsyncClient):
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Registered',
            'name': 'ПФ-115'
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 200

        base_recipe_id = new_response.json()['id']
        response = await client.get(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}', )
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == base_recipe_id
        assert result['document_datetime'] == "2025-04-19T17:00:00Z"
        assert result['name'] == "ПФ-115"
        assert result['status'] == "Registered"
        assert result['commentary'] == "Comment for Base Recipe"
        assert result['rules'] == {}

    async def test_create_base_recipe_success_no_status(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'rules': rules,
            'name': 'ПФ-115'
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 200

        base_recipe_id = new_response.json()['id']
        response = await client.get(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}', )
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == base_recipe_id
        assert result['document_datetime'] == "2025-04-19T17:00:00Z"
        assert result['name'] == "ПФ-115"
        assert result['status'] == "Registered"
        assert result['commentary'] == "Comment for Base Recipe"
        assert result['rules'] == assert_rules

    async def test_create_base_recipe_success_no_name(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        body = {
            "document_datetime": "2021-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'rules': rules,
            'status': 'Registered',
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 200

        base_recipe_id = new_response.json()['id']
        response = await client.get(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}', )
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == base_recipe_id
        assert result['document_datetime'] == "2021-04-19T17:00:00Z"
        assert result['name'] == f"base_recipe_{result['document_number']:03d}_{result['document_datetime'][:4]}"
        assert result['status'] == "Registered"
        assert result['commentary'] == "Comment for Base Recipe"
        assert result['rules'] == assert_rules

    async def test_create_base_recipe_error_no_rules(self, client: AsyncClient):
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115'
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body))
        assert new_response.status_code == 422
        assert new_response.json()['detail'] == "Rules must be provided for posted documents."

    async def test_create_base_recipe_rules_validation(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        empty_materials_rules = deepcopy(rules)
        empty_materials_rules['film_former_part']['materials'] = []
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': empty_materials_rules
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Value error, Materials list must not be empty" in new_response.text

        none_in_materials = empty_materials_rules
        none_in_materials['film_former_part']['materials'] = [{'uuids': [None], 'ratios': [1], 'dosage': None}]
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': none_in_materials
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Set value of nomenclature id in rules.film_former_part.materials.root[0].uuids" in new_response.text

        id1 = deepcopy(rules['film_former_part']['materials'][0]['uuids'][0])
        id2 = deepcopy(rules['film_former_part']['materials'][1]['uuids'][0])
        none_in_materials['film_former_part']['materials'] = \
            [{'uuids': [id1, id2], 'ratios': [None, None], 'dosage': None}]
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': none_in_materials
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Set value of material ratio in rules.film_former_part.materials.root[0].ratios" in new_response.text

        invalid_uuid = deepcopy(RULES_EXAMPLE)
        invalid_uuid['film_former_part']['materials'][0]['uuids'] = ['asdfgsdfgds']
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': invalid_uuid
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Input should be a valid UUID" in new_response.text

        empty_pigment_part = deepcopy(RULES_EXAMPLE)
        empty_pigment_part['pigment_part'] = []
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': empty_pigment_part
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "At least one pigment part with color must be specified" in new_response.text

        no_color = deepcopy(RULES_EXAMPLE)
        no_color['pigment_part'][0]['color'] = None
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': no_color
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Set value of color name in rules.pigment_part[0].color" in new_response.text

        no_dry = deepcopy(RULES_EXAMPLE)
        no_dry['pigment_part'][0]['dry_residue'] = None
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': no_dry
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Set value of dry residue amount in rules.pigment_part[0].dry_residue." in new_response.text

        no_degree = deepcopy(RULES_EXAMPLE)
        no_degree['pigment_part'][0]['pigmentation_degree'] = None
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': no_degree
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Set value of pigmentation_degree in rules.pigment_part[0].pigmentation_degree" in new_response.text

        no_ratio = deepcopy(RULES_EXAMPLE)
        no_ratio['pigment_part'][0]['filler_ratio'] = None
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': no_ratio
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Set value of filler_ratio in rules.pigment_part[0].filler_ratio" in new_response.text

        no_materials = deepcopy(RULES_EXAMPLE)
        no_materials['pigment_part'][0]['materials'] = []
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': no_materials
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Materials for color white must be specified." in new_response.text

        duplicate_color = deepcopy(RULES_EXAMPLE)
        duplicate_color['pigment_part'][1]['color'] = 'white'
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': duplicate_color
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Color 'white' is duplicated" in new_response.text

        no_group_name = deepcopy(RULES_EXAMPLE)
        no_group_name['additives_part']['materials'][0]['nomenclature_group_id'] = None
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': no_group_name
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Set value of rules.additives_part.materials[0].nomenclature_group_id." in new_response.text

        duplicate_group = deepcopy(RULES_EXAMPLE)
        id1 = deepcopy(duplicate_group['additives_part']['materials'][0]['nomenclature_group_id'])
        duplicate_group['additives_part']['materials'][1]['nomenclature_group_id'] = id1
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Posted',
            'name': 'ПФ-115',
            'rules': duplicate_group
        }
        new_response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert new_response.status_code == 422
        assert "Nomenclature group id already defined within rules.additives_part.materials" in new_response.text


    async def test_get_base_recipe_by_id_success(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        body = {
            "document_datetime": "2025-04-19 17:00:10",
            "commentary": "For fetch by id",
            "rules": rules
        }
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 200
        base_recipe_id = response.json()["id"]

        get_response = await client.get(f"/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == base_recipe_id
        assert get_response.json() == response.json()

    async def test_get_base_recipe_invalid_id(self, client: AsyncClient):
        response = await client.get("/api/v1/document/base-recipe/?base_recipe_id=not-a-uuid")
        assert response.status_code == 422

    async def test_get_base_recipe_not_found(self, client: AsyncClient):
        import uuid
        random_uuid = str(uuid.uuid4())
        response = await client.get(f"/api/v1/document/base-recipe/?base_recipe_id={random_uuid}")
        assert response.status_code == 404
    #
    async def test_get_base_recipe_no_id(self, client: AsyncClient):
        response = await client.get("/api/v1/document/base-recipe/")
        assert response.status_code == 422

    async def test_get_all_recipes(self, client: AsyncClient):
        response = await client.get("/api/v1/document/base-recipes/")
        assert response.status_code == 200
        assert len(response.json()) == 8

    async def test_update_base_recipe_not_exist(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        invalid_id = str(uuid.uuid4())
        body = {
            "status": 'Registered',
            "document_datetime": "2025-04-19 13:20:10",
            "commentary": "For update",
            "name": "ГФ-021",
            "rules": rules
        }
        response = await client.patch(f"/api/v1/document/base-recipe/?base_recipe_id={invalid_id}", content=json.dumps(body, default=str))
        assert response.status_code == 404
        assert 'Updating base recipe does not exist.' in response.text

    async def test_update_base_recipe_no_values(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        body = {
            "status": 'Registered',
            "document_datetime": "2025-04-19 13:20:10",
            "commentary": "For update",
            "name": "ГФ-021",
            "rules": rules
        }
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 200
        br_id = response.json()["id"]

        response = await client.patch(f"/api/v1/document/base-recipe/?base_recipe_id={br_id}", content=json.dumps({}))
        assert response.status_code == 422
        assert 'At least one parameter for user update info should be provided' in response.text

    async def test_update_base_recipe(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        body = {
            "status": 'Registered',
            "document_datetime": "2025-04-19 13:20:10",
            "commentary": "For update",
            "name": "ГФ-021",
            "rules": rules
        }
        response = await client.post(f"/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 200
        base_recipe_id = response.json()["id"]

        new_rules = deepcopy(RULES_EXAMPLE)
        new_rules['pigment_part'][0]['color'] = 'Красно-коричневый'

        assert_rules = json.loads(json.dumps(new_rules, default=str))

        new_body = {
            "status": 'Posted',
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Updated",
            "name": "ГФ-021 б/с",
            "rules": new_rules
        }

        response = await client.patch(
            f"/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}", content=json.dumps(new_body, default=str)
        )

        assert response.status_code == 200
        assert response.json()["id"] == base_recipe_id
        assert response.json()["rules"] == assert_rules
        assert response.json()["rules"]['pigment_part'][0]['color'] == 'Красно-коричневый'
        assert response.json()["status"] == 'Posted'
        assert response.json()["name"] == "ГФ-021 б/с"
        assert response.json()["commentary"] == "Updated"
        assert response.json()["document_datetime"] == "2025-04-19T17:00:00"


    async def test_update_base_recipe_no_new_rules(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        body = {
            "status": 'Registered',
            "document_datetime": "2025-04-19 13:20:10",
            "commentary": "For update",
            "name": "ГФ-021",
            "rules": rules
        }
        response = await client.post(f"/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 200
        base_recipe_id = response.json()["id"]

        patch_body = {
            "status": "Registered",  # статус не меняем
            "name": "ГФ-021 (v2)",
            "commentary": "Only meta updated",
            "document_datetime": "2025-04-20 10:00:00",
        }

        response = await client.patch(
            f"/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}",
            content=json.dumps(patch_body, default=str),
        )
        assert response.status_code == 200
        response = response.json()

        assert response["rules"] == assert_rules
        assert response["name"] == "ГФ-021 (v2)"
        assert response["commentary"] == "Only meta updated"
        assert response["document_datetime"] == "2025-04-20T10:00:00"
        assert response["status"] == "Registered"


    async def test_update_base_recipe_set_posted_when_invalid_rules_in_db(self, client: AsyncClient):
        no_color = deepcopy(RULES_EXAMPLE)
        no_color['pigment_part'][0]['color'] = None
        no_color['is_posted'] = False
        body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Comment for Base Recipe",
            'status': 'Registered',
            'name': 'ПФ-115',
            'rules': no_color
        }
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 200
        base_recipe_id = response.json()["id"]

        patch_body = {
            "status": "Posted",
            "commentary": "try make Posted",
        }
        new_response = await client.patch(
            f"/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}",
            content=json.dumps(patch_body, default=str),
        )
        assert new_response.status_code == 422
        assert "Set value of color name in rules.pigment_part[0].color" in new_response.text


    async def test_update_base_recipe_some_fields(self, client: AsyncClient):
        rules = deepcopy(RULES_EXAMPLE)
        assert_rules = json.loads(json.dumps(rules, default=str))
        body = {
            "status": 'Registered',
            "document_datetime": "2025-04-19 13:20:10",
            "commentary": "For update",
            "rules": rules,
        }
        response = await client.post(f"/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 200
        base_recipe_id = response.json()["id"]

        new_rules = deepcopy(RULES_EXAMPLE)

        new_rules['pigment_part'][0]['color'] = 'Красно-коричневый'

        new_body = {
            "name": "ГФ-021 б/с",
            "rules": new_rules,
            "hihi": 1
        }

        response = await client.patch(
            f"/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}", content=json.dumps(new_body, default=str)
        )

        assert response.status_code == 200
        assert response.json()["id"] == base_recipe_id
        assert response.json()["rules"] != assert_rules
        assert response.json()["rules"]['pigment_part'][0]['color'] == 'Красно-коричневый'
        assert response.json()["status"] == 'Registered'
        assert response.json()["name"] == "ГФ-021 б/с"
        assert response.json()["commentary"] == "For update"
        assert response.json()["document_datetime"] == "2025-04-19T13:20:10Z"
        assert response.json().get("hihi") is None

    async def test_delete_base_recipe_not_exist(self, client):
        response = await client.delete("/api/v1/document/base-recipe/?base_recipe_id=3fa85f64-5717-4562-b3fc-2c963f66afa6")
        assert response.status_code == 404
        assert response.json() == {'detail': 'Base recipe does not exist.'}

    async def test_delete_base_recipe(self, client):
        rules = deepcopy(RULES_EXAMPLE)
        body = {
            "status": 'Registered',
            "document_datetime": "2025-04-19 13:20:10",
            "commentary": "For update",
            "name": "ГФ-021",
            "rules": rules
        }
        response = await client.post(f"/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 200
        base_recipe_id = response.json()["id"]

        del_response = await client.delete(f'/api/v1/document/base-recipe/?base_recipe_id={base_recipe_id}')
        assert del_response.status_code == 200
        assert del_response.json()['id'] == base_recipe_id
        assert del_response.json()['document_number'] == response.json()['document_number']
        assert del_response.json()['name'] == "ГФ-021"
        assert del_response.json()['document_datetime'] == '2025-04-19T13:20:10Z'

    async def test_create_base_recipe_validate_ids(self, client: AsyncClient):
        base_body = {
            "document_datetime": "2025-04-19 17:00:00",
            "commentary": "Тестовая проверка с несуществующим UUID",
            "status": "Posted",
            "name": "ПФ-115"
        }

        rules = deepcopy(RULES_EXAMPLE)
        rules["film_former_part"]["materials"][0]["uuids"][0] = uuid.uuid4()
        body = {**base_body, "rules": rules}
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 422
        assert "nomenclature id(s) not found:" in response.text.lower()

        rules = deepcopy(RULES_EXAMPLE)
        rules["pigment_part"][0]["materials"][0]["items"][0]["uuids"][0] = uuid.uuid4()
        body = {**base_body, "rules": rules}
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 422
        assert "nomenclature id(s) not found:" in response.text.lower()

        rules = deepcopy(RULES_EXAMPLE)
        rules["additives_part"]["materials"][1]["items"][0]["uuids"][0] = uuid.uuid4()
        body = {**base_body, "rules": rules}
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 422
        assert "nomenclature id(s) not found:" in response.text.lower()

        rules = deepcopy(RULES_EXAMPLE)
        rules["additives_part"]["materials"][2]["nomenclature_group_id"] = uuid.uuid4()
        body = {**base_body, "rules": rules}
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 422
        assert "NomenclatureGroup id(s) not found:" in response.text

        rules = deepcopy(RULES_EXAMPLE)
        rules["solvent_part"]["materials"][0]["uuids"][0] = uuid.uuid4()
        body = {**base_body, "rules": rules}
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 422
        assert "nomenclature id(s) not found:" in response.text.lower()

        rules = deepcopy(RULES_EXAMPLE)
        rules["pigment_part"][0]["materials"][0]["nomenclature_group_id"] = uuid.uuid4()
        body = {**base_body, "rules": rules}
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 422
        assert response.json() == {'detail': 'There is no group "Пигменты" in pigment part.'}

        rules = deepcopy(RULES_EXAMPLE)
        rules["pigment_part"][1]["materials"][1]["nomenclature_group_id"] = uuid.uuid4()
        body = {**base_body, "rules": rules}
        response = await client.post("/api/v1/document/base-recipe/", content=json.dumps(body, default=str))
        assert response.status_code == 422
        assert response.json() == {'detail': 'There is no group "Наполнители" in pigment part.'}
