# coding: utf-8

"""
    Data Modelling Storage Service API

    Data storage service for DMT  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import dmss_api
from dmss_api.models.inline_response2001 import InlineResponse2001  # noqa: E501
from dmss_api.rest import ApiException

class TestInlineResponse2001(unittest.TestCase):
    """InlineResponse2001 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse2001
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = dmss_api.models.inline_response2001.InlineResponse2001()  # noqa: E501
        if include_optional :
            return InlineResponse2001(
                uid = '0'
            )
        else :
            return InlineResponse2001(
        )

    def testInlineResponse2001(self):
        """Test InlineResponse2001"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
