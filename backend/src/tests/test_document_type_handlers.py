import json


class TestDocumentTypeHandlers:
    async def test_get_all_document_types_not_exist(self, client):
        response = await client.get('/api/v1/document-types/')
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_all_document_types(self, client):
        response = await client.get('/api/v1/document-types/')
        assert response.status_code == 200
        assert response.json() == []
