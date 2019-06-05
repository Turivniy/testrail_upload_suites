#!/usr/bin/env python
#
#    Copyright 2017 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys

from base import Base
import config

import logging


logging.basicConfig(
    format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    handlers=[logging.FileHandler('{}{}'.format(
        config.LOG_FOLDER, config.LOG_FILENAME)), logging.StreamHandler()],
    level=logging.INFO)
logger = logging.getLogger(config.LOGGER)


def choose_section_by_test_name(test_name):
    for section, key_words in config.SECTIONS_MAP.items():
        for key_word in key_words:
            if key_word in test_name:
                return section

    return "Other"


def get_tags_by_test_name(test_name):
    tags = []
    if test_name.find("[") > -1:
        tags = test_name.split("[")[1][:-1].split(",")
    return tags


def create_tr_test_cases(test_cases, milestone_id, type_id=1, priority_id=4,
                         qa_team=4):
    tr_test_cases = []

    for test_case_name in test_cases:
        section = choose_section_by_test_name(test_case_name)
        if section not in config.SECTIONS_MAP:
            config.SECTIONS_MAP[section] = []
        test_class, test_name = test_case_name.rsplit(".", 1)

        report_label = test_name
        for tag in get_tags_by_test_name(test_name):
            if tag.startswith("id-"):
                report_label = tag[3:]
                break

        test_case = {
            "milestone_id": milestone_id,
            "section": section,
            "title": (("%s.%s" % (test_class, test_name)) if config.USE_TEST_IDs
                      else test_name),
            "type_id": type_id,
            "priority_id": priority_id,
            "custom_qa_team": qa_team,
            "estimate": "1m",
            "refs": "",
            "custom_test_group": test_class,
            "custom_test_case_description": test_name,
            "custom_test_case_steps": [{"Run test": "passed"}],
            "custom_report_label": report_label
        }
        tr_test_cases.append(test_case)

    return tr_test_cases


def _add_tr_test_case(tr_client, suite_id, tr_test_case):
    for i in range(7):
        try:
            tr_client.add_case(suite_id, tr_test_case)
        except APIError:
            logging.info("APIError")
        else:
            break


def main():
    call = Base()
    try:
        tests_file_path = sys.argv[1]
    except IndexError:
        raise Exception("Path to a tests file should be provided!")

    if os.path.exists(tests_file_path):
        logger.info("Reading tests file '%s'..." % tests_file_path)
        with open(tests_file_path) as f:
            test_cases = [test for test in f.read().split("\n") if test]
            logger.info("Tests file '%s' has been successfully read."
                        % tests_file_path)
    else:
        raise Exception("Tests file '%s' doesn't exist!" % tests_file_path)

    logger.info("Initializing TestRail client...")
    logger.info("TestRail client has been successfully initialized.")
    logger.info("Getting milestone '%s'..." % config.MILESTONE)

    milestone = call.get_milestone_by_name(config.MILESTONE)

    logger.info(milestone)
    logger.info("Getting tests suite '%s'..." % config.SUITE)

    suite = call.get_suite_by_name(config.SUITE)
    if not suite:
        logger.info("Tests suite '%s' not found. "
                    "Creating tests suite..." % config.SUITE)

        suite = call.add_suite(config.SUITE)
        logger.info("Tests suite has benn successfully created.")
    logger.info(suite)

    logger.info("Creating test cases for TestRail...")
    tr_test_cases = create_tr_test_cases(
        test_cases, milestone["id"],
        type_id=config.TEST_CASE_TYPE_ID,
        priority_id=config.TEST_CASE_PRIORITY_ID,
        qa_team=config.QA_TEAM)
    logger.info("Test cases have been successfully created.")

    # #### There are no method called delete_section() in the Base class ###
    # if config.DELETE_OLD_SECTIONS:
    #     logger.info("Deleting old sections...")
    #     old_sections = call.get_sections(suite["id"])
    #     for section in old_sections:
    #         if section["parent_id"] is None:
    #             call.delete_section(section["id"])
    #     logger.info("Old sections have been successfully deleted.")

    sections_map = {}
    for section in sorted(config.SECTIONS_MAP.keys()):
        logger.info("Creating section '%s'..." % section)
        s = call.add_section(suite["id"], section)
        logger.info("Section '%s' has been successfully created." % section)
        sections_map[section] = s["id"]

    logger.info("Uploading created test cases to TestRail...")

    for t in tr_test_cases:
        _add_tr_test_case(call, sections_map[t["section"]], t)
    logger.info("Test cases have been successfully uploaded.")


if __name__ == "__main__":
    main()
