# testrail_upload_suites
## How to Description:

1. Clone the repository `testrail_upload_suites`, for example:

    ~~~~
    git clone https://github.com/Turivniy/testrail_upload_suites.git
    ~~~~

2. Install python 3.6 virtualenv:

    ~~~~
    apt install python3.6-venv
    ~~~~

3. Navigate to the `testrail_upload_suites/` folder:
   ~~~
   cd testrail_upload_suites/
   ~~~

4. Create virtualenv and activate this:

    ~~~~
    virtualenv --python=python3.6 .venv
    . .venv/bin/activate
    ~~~~

5. In the `testrail_upload_suites` folder install requirements:

    ~~~~
    pip3 install -r requirements.txt
    ~~~~

6. In the environment set bash variables
    ```bash
    export TESTRAIL_URL='https://mirantis.testrail.com'
    export TESTRAIL_PROJECT='Mirantis Cloud Platform'
    export TESTRAIL_USER='you testrail username, for example sturivnyi@mirantis.com'
    export TESTRAIL_PASSWORD='you super secret password'
    export TESTRAIL_MILESTONE='MCP1.1 for example'
    export TESTRAIL_SUITE='A new suite where tests will be uploaded'
    ```

7. Edit `SECTION_MAP` in the `config.py` file:
   Comment sections that you do not want to be uploaded to the Testrail Suites.
   There is `# "Barbican": ["barbican_tempest_plugin."]` section is commented.
    ```python
     SECTIONS_MAP = {
        "Telemetry": ["telemetry_tempest_plugin."],
        "Glance": ["image."],
        "Keystone": ["identity."],
        "Neutron": ["network."],
        "Nova": ["compute."],
        "Swift": ["object_storage."],
        "Scenario": ["tempest.scenario."],
        "Manila": ["manila_tempest_tests."],
        "Ironic": ["ironic_tempest_plugin."],
        "Heat": ["heat_tempest_plugin."],
        "Designate": ["designate_tempest_plugin."],
        # "Barbican": ["barbican_tempest_plugin."],
        "Horizon": ["tempest_horizon."]
     }
    ```

8. Prepare file with the tests for upload. 
   For example, `tests_for_upload.txt` the file with the tests that go one by one.
   
    ```
    ...
    tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard
    tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers
    tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details
    tempest.api.compute.test_versions.TestVersions.test_get_version_details
    tempest.api.compute.test_versions.TestVersions.test_list_api_versions
    ...
    ```
    
9. Upload thests to the testrail. In this example the command will be:

    ~~~
    python upload_suite.py tests_for_upload.txt
    ~~~
