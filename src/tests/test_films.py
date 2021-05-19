import http
import json
from dataclasses import dataclass
from unittest.mock import patch

from src import app


@dataclass
class FakeFilm:
    title = 'Fake Film'
    distributed_by = 'Fake'
    release_date = '2002-12-03'
    description = 'Fake description'
    length = 100
    rating = 8.0


class TestFilms:
    uuid = []
    fake_film = {
        'title': 'Test Title',
        'distributed_by': 'Test Company',
        'release_date': '2010-04-01',
        'description': '',
        'length': 100,
        'rating': 8.0
    }

    def test_get_films_with_db(self):
        client = app.test_client()
        response = client.get('/films')

        assert response.status_code == http.HTTPStatus.OK

    @patch('src.services.film_service.FilmService.fetch_all_films', autospec=True)
    def test_get_films_with_mock_db(self, mock_db_call):
        client = app.test_client()
        response = client.get('/films')

        mock_db_call.assert_called_once()
        assert response.status_code == http.HTTPStatus.OK
        assert len(response.json) == 0

    def test_create_film_with_db(self):
        client = app.test_client()
        response = client.post('/films', data=json.dumps(self.fake_film), content_type='application/json')

        assert response.status_code == http.HTTPStatus.CREATED
        assert response.json["title"] == self.fake_film["title"]
        self.uuid.append(response.json["uuid"])

    def test_create_film_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add,  \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            response = client.post('/films', data=json.dumps(self.fake_film), content_type='application/json')

            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            assert response.status_code == http.HTTPStatus.CREATED
            assert response.json["title"] == self.fake_film["title"]

    def test_update_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        new_data = {
            'title': 'Update Title',
            'distributed_by': 'update',
            'release_date': '2010-04-01'
        }
        response = client.put(url, data=json.dumps(new_data), content_type='application/json')

        assert response.status_code == http.HTTPStatus.OK
        assert response.json["title"] == new_data["title"]

    def test_update_film_with_mock_db(self):
        with patch('src.services.film_service.FilmService.fetch_film_by_uuid') as mocked_query, \
                patch('src.db.session.add', autospec=True) as mock_session_add,  \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeFilm()

            client = app.test_client()
            url = f'/films/1'
            new_data = {
                'title': 'Update Title',
                'distributed_by': 'update',
                'release_date': '2010-04-01'
            }

            client.put(url, data=json.dumps(new_data), content_type='application/json')

            mocked_query.assert_called_once()
            mock_session_commit.assert_called_once()
            mock_session_add.assert_called_once()

    def test_delete_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        response = client.delete(url)

        assert response.status_code == http.HTTPStatus.NO_CONTENT

# todo: coverage via pycharm
