#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from leginorma import LegifranceClient, LegifranceText


def test_client():
    client = LegifranceClient(os.environ['LEGIFRANCE_CLIENT_ID'], os.environ['LEGIFRANCE_CLIENT_SECRET'])
    LegifranceText.from_dict(client.consult_law_decree('JORFTEXT000034429274'))
