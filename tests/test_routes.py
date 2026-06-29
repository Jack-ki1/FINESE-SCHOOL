"""Tests for main routes."""
import json


class TestMainRoutes:
    def test_index(self, client):
        res = client.get('/')
        assert res.status_code == 200
        assert b'FINESE SCHOOL' in res.data

    def test_workspace(self, client):
        res = client.get('/workspace')
        assert res.status_code == 200
        assert b'SQL Editor' in res.data

    def test_settings(self, client):
        res = client.get('/settings')
        assert res.status_code == 200

    def test_learning_hub(self, client):
        res = client.get('/learn/')
        assert res.status_code == 200
        assert b'Learning' in res.data


class TestChatAPI:
    def test_create_conversation(self, client):
        res = client.post('/api/conversations',
                          data=json.dumps({'title': 'Test Chat'}),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['conversation']['title'] == 'Test Chat'

    def test_list_conversations(self, client):
        # Create a conversation first
        client.post('/api/conversations',
                     data=json.dumps({'title': 'Test'}),
                     content_type='application/json')
        res = client.get('/api/conversations')
        assert res.status_code == 200
        data = res.get_json()
        assert len(data['conversations']) >= 1

    def test_get_settings(self, client):
        res = client.get('/api/settings')
        assert res.status_code == 200
        data = res.get_json()
        assert 'provider' in data

    def test_update_settings(self, client):
        res = client.post('/api/settings',
                          data=json.dumps({'temperature': 0.5}),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['temperature'] == 0.5

    def test_get_providers(self, client):
        res = client.get('/api/providers')
        assert res.status_code == 200
        data = res.get_json()
        assert 'providers' in data
        assert 'openai' in data['providers']
