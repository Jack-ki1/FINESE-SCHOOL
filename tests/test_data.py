"""Tests for data routes (SQL, code execution, data analysis)."""
import json
import io


class TestDataRoutes:
    def test_create_sample_db(self, client):
        res = client.post('/data/sample-db')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert data['connection'] == 'sample_db'

    def test_list_connections(self, client):
        res = client.get('/data/connections')
        assert res.status_code == 200
        data = res.get_json()
        assert 'connections' in data

    def test_create_sqlite_connection(self, client):
        res = client.post('/data/connections',
                          data=json.dumps({
                              'name': 'test_db',
                              'db_type': 'sqlite',
                              'path': ':memory:'
                          }),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True

    def test_execute_sql_no_connection(self, client):
        res = client.post('/data/sql/execute',
                          data=json.dumps({
                              'connection': 'nonexistent',
                              'sql': 'SELECT 1'
                          }),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is False

    def test_execute_sql_with_sample_db(self, client):
        # Create sample DB first
        client.post('/data/sample-db')

        res = client.post('/data/sql/execute',
                          data=json.dumps({
                              'connection': 'sample_db',
                              'sql': 'SELECT * FROM customers'
                          }),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert data['row_count'] == 5

    def test_get_schema(self, client):
        client.post('/data/sample-db')
        res = client.get('/data/sql/schema?connection=sample_db')
        assert res.status_code == 200
        data = res.get_json()
        assert 'tables' in data
        assert 'customers' in data['tables']

    def test_list_datasets_empty(self, client):
        res = client.get('/data/datasets')
        assert res.status_code == 200
        data = res.get_json()
        assert 'datasets' in data

    def test_execute_code_empty(self, client):
        res = client.post('/data/code/execute',
                          data=json.dumps({'code': 'print("hello")'}),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert 'hello' in data['output']

    def test_execute_code_error(self, client):
        res = client.post('/data/code/execute',
                          data=json.dumps({'code': 'raise ValueError("test error")'}),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is False

    def test_upload_csv(self, client):
        data = {
            'file': (io.BytesIO(b'name,age\nAlice,30\nBob,25'), 'test.csv'),
        }
        res = client.post('/api/upload',
                          data=data,
                          content_type='multipart/form-data')
        assert res.status_code == 200
        result = res.get_json()
        assert result['success'] is True


class TestEducationRoutes:
    def test_learning_hub(self, client):
        res = client.get('/learn/')
        assert res.status_code == 200

    def test_get_paths(self, client):
        res = client.get('/learn/api/paths')
        assert res.status_code == 200
        data = res.get_json()
        assert 'paths' in data
        assert len(data['paths']) > 0

    def test_get_exercises(self, client):
        res = client.get('/learn/api/modules/sql-1/exercises')
        assert res.status_code == 200
        data = res.get_json()
        assert 'exercises' in data
        assert len(data['exercises']) > 0

    def test_check_exercise_correct(self, client):
        res = client.post('/learn/api/exercises/sql-1-1/check',
                          data=json.dumps({
                              'answer': 'SELECT * FROM customers'
                          }),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['correct'] is True

    def test_check_exercise_incorrect(self, client):
        res = client.post('/learn/api/exercises/sql-1-1/check',
                          data=json.dumps({
                              'answer': 'WRONG ANSWER'
                          }),
                          content_type='application/json')
        assert res.status_code == 200
        data = res.get_json()
        assert data['correct'] is False

    def test_get_hint(self, client):
        res = client.get('/learn/api/exercises/sql-1-1/hint')
        assert res.status_code == 200
        data = res.get_json()
        assert 'hint' in data

    def test_get_progress(self, client):
        res = client.get('/learn/api/progress')
        assert res.status_code == 200
        data = res.get_json()
        assert 'progress' in data
