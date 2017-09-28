# Copyright (c) 2017 Intel Corporation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import unittest

from django.test import Client
from rest_framework import status

from newton.requests.tests import mock_info
from newton.requests.tests import test_base
from newton.requests.views.util import VimDriverUtils


MOCK_GET_LIMITS_RESPONSE = {
    "limits": {
        "absolute": {
            "id": "uuid_1", "name": "limit_1"
        }
    }
}

MOCK_GET_QUOTAS_RESPONSE = {
    "quota": {"limit": "1"}
}


class TestLimit(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    @staticmethod
    def _get_mock_response(return_value=None):
        mock_response = mock.Mock(spec=test_base.MockResponse)
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = return_value
        return mock_response

    @mock.patch.object(VimDriverUtils, 'get_session')
    @mock.patch.object(VimDriverUtils, 'get_vim_info')
    def test_get_limits_list(self, mock_get_vim_info, mock_get_session):

        mock_get_session.return_value = test_base.get_mock_session(
            ["get"], {
                "side_effect": [
                    self._get_mock_response(MOCK_GET_LIMITS_RESPONSE),
                    self._get_mock_response(MOCK_GET_QUOTAS_RESPONSE),
                    self._get_mock_response(MOCK_GET_LIMITS_RESPONSE)
                ]
            })

        mock_get_vim_info.return_value = mock_info.MOCK_VIM_INFO

        response = self.client.get(
            "/api/multicloud-newton/v0/windriver-hudson-dc_RegionOne/fcca3cc49d5e42caae15459e27103efc/limits",
            {}, HTTP_X_AUTH_TOKEN=mock_info.MOCK_TOKEN_ID)

        context = response.json()
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(context)
        self.assertIn(
            MOCK_GET_LIMITS_RESPONSE["limits"]["absolute"]['id'], context['id'])

    @mock.patch.object(VimDriverUtils, 'get_session')
    @mock.patch.object(VimDriverUtils, 'get_vim_info')
    def test_get_limits_list_failure(self, mock_get_vim_info, mock_get_session):

        mock_get_session.return_value = test_base.get_mock_session(
            ["get"], {
                "side_effect": [
                    self._get_mock_response(MOCK_GET_LIMITS_RESPONSE),
                    self._get_mock_response({}),
                    self._get_mock_response(MOCK_GET_LIMITS_RESPONSE)
                ]
            })

        mock_get_vim_info.return_value = mock_info.MOCK_VIM_INFO

        response = self.client.get(
            "/api/multicloud-newton/v0/windriver-hudson-dc_RegionOne/fcca3cc49d5e42caae15459e27103efc/limits",
            {}, HTTP_X_AUTH_TOKEN=mock_info.MOCK_TOKEN_ID)

        context = response.json()
        self.assertIn('error', context)
        self.assertEquals(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
