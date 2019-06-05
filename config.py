import os

MILESTONE = os.environ.get('TESTRAIL_MILESTONE')
SUITE = os.environ.get('TESTRAIL_SUITE')
PROJECT = os.environ.get('TESTRAIL_PROJECT')
URL = os.environ.get('TESTRAIL_URL')
USER = os.environ.get('TESTRAIL_USER')
PASSWORD = os.environ.get('TESTRAIL_PASSWORD')
PLAN_NAME = os.environ.get('TESTRAIL_PLAN_NAME')
RESULT = os.environ.get('TESTRAIL_RESULT')


# Use test IDs for titles of TestRail test cases like
# 'tempest.api.identity.admin.v2.test_rolesRolesTestJSON.test_list_roles[id-
# 75d9593f-50b7-4fcf-bd64-e3fb4a278e23]' instead of test names.
USE_TEST_IDs = True

TEST_CASE_TYPE_ID = 1  # Automated
TEST_CASE_PRIORITY_ID = 4  # P0
QA_TEAM = 4  # MOS
DELETE_OLD_SECTIONS = False  # User should have proper permissions to do it
UPLOAD_THREADS_COUNT = 4

SECTIONS_MAP = {
     "Telemetry": ["telemetry_tempest_plugin."],
     "Glance": ["image."],
     "Keystone": ["identity."],
     "Neutron": ["network."],
     "Nova": ["compute."],
     "Swift": ["object_storage."],
     "Scenario": ["tempest.scenario."],
     "Manila": ["manila_tempest_tests"],
     "Ironic": ["ironic_tempest_plugin."],
     "Heat": ["heat_tempest_plugin."],
     "Designate": ["designate_tempest_plugin."],
     "Barbican": ["barbican_tempest_plugin."],
     "Horizon": ["tempest_horizon."]
}

# Logging
LOGGER = 'upload_suite'
LOG_FOLDER = '/tmp/'
LOG_FILENAME = 'upload_suite.log'
