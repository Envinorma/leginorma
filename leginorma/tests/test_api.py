#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import pytest
import responses
from requests_oauthlib.oauth2_session import OAuth2Session

from leginorma import LegifranceClient, LegifranceText
from leginorma.api import _API_HOST, LegifranceRequestError, _post_request


def test_client():
    client = LegifranceClient(os.environ['LEGIFRANCE_CLIENT_ID'], os.environ['LEGIFRANCE_CLIENT_SECRET'])
    client.consult_law_decree('JORFTEXT000034429274')


def test_client_law_decree():
    client = LegifranceClient(os.environ['LEGIFRANCE_CLIENT_ID'], os.environ['LEGIFRANCE_CLIENT_SECRET'])
    LegifranceText.from_dict(client.consult_law_decree('JORFTEXT000034429274'))


def test_client_jorf():
    client = LegifranceClient(os.environ['LEGIFRANCE_CLIENT_ID'], os.environ['LEGIFRANCE_CLIENT_SECRET'])
    LegifranceText.from_dict(client.consult_jorf('JORFTEXT000034429274'))


@responses.activate
def test_post_request():
    responses.add(responses.POST, _API_HOST + '/consult/lawDecree', json={'title': 'text title'}, status=200)

    resp = _post_request('/consult/lawDecree', {}, OAuth2Session(''))
    assert resp == {'title': 'text title'}


@responses.activate
def test_post_request_2():
    responses.add(responses.POST, _API_HOST + '/consult/lawDecree', json={'error': 'error'}, status=400)

    with pytest.raises(LegifranceRequestError):
        _post_request('/consult/lawDecree', {}, OAuth2Session(''))
