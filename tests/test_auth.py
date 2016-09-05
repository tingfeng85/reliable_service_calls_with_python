#!/usr/bin/env python
# encoding: utf-8
from unittest import mock
from falcon.testing import TestCase

from auth import AuthenticationResource


class TestAuthentication(TestCase):
    def setUp(self):
        super().setUp()
        self.api.add_route('/authenticate', AuthenticationResource())

    def test_token_is_required(self):
        resp = self.simulate_post('/authenticate')
        assert 401 == resp.status_code

    @mock.patch('uuid.uuid4')
    def test_user_details_with_valid_token(self, mock_uuid4):
        mock_uuid4.return_value = '1234'
        resp = self.simulate_post('/authenticate', headers={"Authorization": "1234"})
        expected_data = {
            'uuid': '1234',
            'permissions': ['can_view_recommendations', 'can_view_homepage']
        }
        assert 200 == resp.status_code
        assert expected_data == resp.json