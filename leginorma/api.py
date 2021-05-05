import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from requests_oauthlib import OAuth2Session

_API_HOST = 'https://api.aife.economie.gouv.fr/dila/legifrance-beta/lf-engine-app'
_TOKEN_URL = 'https://oauth.aife.economie.gouv.fr/api/oauth/token'


def _get_legifrance_client(client_id: str, client_secret: str) -> OAuth2Session:
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'openid',
    }
    response = requests.post(_TOKEN_URL, data=data)
    if 200 <= response.status_code < 300:
        token = response.json()
        client = OAuth2Session(client_id, token=token)
        return client
    raise LegifranceRequestError(f'Error when retrieving token: {response.json()}')


HOUR = 60 * 60


def _extract_response_content(response: requests.Response) -> Dict:
    if 200 <= response.status_code < 300:
        return response.json()
    raise LegifranceRequestError(
        f'Request has status_code {response.status_code} and content {response.content.decode()}'
    )


def _request_consult_law_decree(cid: str, date: datetime, client: OAuth2Session) -> requests.Response:
    json_ = {'date': int(date.timestamp()) * 1000, 'textId': cid}
    url = _API_HOST + '/consult/lawDecree'
    return client.post(url, json=json_)


def _article_by_id(article_id: str, client: OAuth2Session) -> Dict:
    json_ = {'id': article_id}
    url = _API_HOST + '/consult/getArticle'
    response = client.post(url, json=json_)
    return _extract_response_content(response)


def _consult_law_decree(cid: str, date: Optional[datetime], client: OAuth2Session) -> Dict:
    return _extract_response_content(_request_consult_law_decree(cid, date or datetime.now(), client))


class LegifranceClient:
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize Legifrance client with client_id and client_secret.

        Parameters
        ----------
        client_id: str
            client_id provided by Legifrance
        client_secret: str
            client_secret provided by Legifrance
        """
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._client: OAuth2Session = _get_legifrance_client(client_id, client_secret)
        self._last_compute_time = time.time()

    def __exit__(self, *args):
        self._client.close()

    def _update_client_if_necessary(self) -> None:
        elapsed = time.time() - self._last_compute_time
        if elapsed >= HOUR:
            self._last_compute_time = time.time()
            self._client = _get_legifrance_client(self._client_id, self._client_secret)

    def consult_law_decree(self, text_id: str, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Fetches the version of a law/decree/arrete by text identifier for a specific date.

        Parameters
        ----------
        text_id: str
            Identifier of the text
        date: Optional[datetime]
            Date of the version to retrieve. Default to datetime.now()
        """
        self._update_client_if_necessary()
        return _consult_law_decree(text_id, date, self._client)

    def consult_article(self, article_id: str) -> Dict[str, Any]:
        """
        Fetches article by id

        Parameters
        ----------
        article_id: str
            Identifier of the article
        """
        self._update_client_if_necessary()
        return _article_by_id(article_id, self._client)


class LegifranceRequestError(Exception):
    pass
