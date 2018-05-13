import errno
import json
import os
from os import path
from unittest import TestCase

import tests
from tests import tools, GENERATE_CALL_GRAPHS, CALL_GRAPHS_PATH
import exjson

__author__ = 'prods'
__project__ = 'xjson'


class EXJSONTestScenarios(object):
    def load_simple_json(self):
        return (exjson.load("./samples/clean-simple.json"), {
            "Name": "Sample Values",
            "Enabled": True,
            "Values": [
                "A",
                "AB",
                "ABC"
            ],
            "Count": 3
        })

    def load_json_with_comments(self):
        return (exjson.load("./samples/pipeline.stage.001.json", encoding='utf-8'), {
            "Name": "First Stage",
            "Description": "Retrieves Sample Data from file",
            "Sequence_Id": 1,
            "Parameters": {
            },
            "Steps": [
                {
                    "Name": "Get Data",
                    "Description": "This is a sample get data step",
                    "Sequence_Id": 1,
                    "Parameters": {
                    },
                    "Provider": "",
                    "Properties": {
                        "Stop_On_Error": True
                    },
                    "Enabled": True
                }
            ],
            "Enabled": True
        })

    def load_json_with_comments_and_included_files(self):
        return (exjson.load("./samples/pipeline.json", encoding='utf-8'), {
            "Name": "Sample Pipeline",
            "Description": "This is a sample Pipeline",
            "Sequence_Id": 0,
            "Parameters": {
            },
            "Properties": {
            },
            "Stages": [
                {
                    "Name": "First Stage",
                    "Description": "Retrieves Sample Data from file",
                    "Sequence_Id": 1,
                    "Parameters": {
                    },
                    "Steps": [
                        {
                            "Name": "Get Data",
                            "Description": "This is a sample get data step",
                            "Sequence_Id": 1,
                            "Parameters": {
                            },
                            "Provider": "",
                            "Properties": {
                                "Stop_On_Error": True
                            },
                            "Enabled": True
                        }
                    ],
                    "Enabled": True
                },
                {
                    "Name": "Second Stage",
                    "Description": "Retrieves Sample Data from file",
                    "Sequence_Id": 2,
                    "Parameters": {
                        "Dataset": "$.Stages.FirstStage.Steps.GetData.Result"
                    },
                    "Steps": [
                        {
                            "Name": "Transform Data",
                            "Description": "",
                            "Sequence_Id": 1,
                            "Parameters": {
                                "Parameter": "a"
                            },
                            "Provider": "NullProvider",
                            "Properties": {
                                "Stop_On_Error": True
                            },
                            "Enabled": True
                        },
                        {
                            "Name": "Save Data",
                            "Description": "",
                            "Sequence_Id": 2,
                            "Parameters": {

                            },
                            "Provider": "",
                            "Properties": {
                                "Stop_On_Error": True
                            },
                            "Enabled": True
                        }
                    ],
                    "Enabled": True
                }
            ],
            "Enabled": True
        })

    def load_json_in_different_positions(self):
        return (exjson.load("./samples/multi-include.json", encoding='utf-8'), {
            "Name": "Test Name",
            "Values": [
                {
                    "Value_id": "0AEC4D9BC52AB96E424CD057A59CC45EFF314107",
                    "Value": "test message 1"
                },
                {
                    "Value_id": "FFEB4A18FF1C37E59290C86B92DF28F65DB584D9",
                    "Value": "test message"
                }
            ],
            "Other1": {
                "Value_id": "512D4C2E2A63AC8C385A1E2315ABCF4B3D5C7A9F",
                "Value": "test message 2"
            },
            "Other2": "Test Value",
            "Other3": {
                "Value_id": "4034A54700430B6A37E56B5C38070F6B1F333B7B",
                "Value": "test message 2"
            }
        })

    def loads_simple_json_string(self, json_source):
        return (exjson.loads(json_source, encoding='utf-8'), {
            "Name": "Sample Values",
            "Enabled": True,
            "Values": [
                "A",
                "AB",
                "ABC"
            ],
            "Count": 3
        })

    def loads_with_includes_and_no_provided_includes_path(self, json_source):
        return (exjson.loads(json_source, encoding='utf-8'), {
            "Name": "Test",
            "Value": {
                "Name": "Sample Values",
                "Enabled": True,
                "Values": [
                    "A",
                    "AB",
                    "ABC"
                ],
                "Count": 3
            },
            "Enabled": True
        })

    def loads_json_string_with_comments(self, json_source):
        return (exjson.loads(json_source, encoding='utf-8'), {
            "Name": "First Stage",
            "Description": "Retrieves Sample Data from file",
            "Sequence_Id": 1,
            "Parameters": {
            },
            "Steps": [
                {
                    "Name": "Get Data",
                    "Description": "This is a sample get data step",
                    "Sequence_Id": 1,
                    "Parameters": {
                    },
                    "Provider": "",
                    "Properties": {
                        "Stop_On_Error": True
                    },
                    "Enabled": True
                }
            ],
            "Enabled": True
        })

    def loads_json_with_comments_and_included_files(self, json_source):
        return (exjson.loads(json_source, encoding='utf-8', includes_path="./samples"), {
            "Name": "Sample Pipeline",
            "Description": "This is a sample Pipeline",
            "Sequence_Id": 0,
            "Parameters": {
            },
            "Properties": {
            },
            "Stages": [
                {
                    "Name": "First Stage",
                    "Description": "Retrieves Sample Data from file",
                    "Sequence_Id": 1,
                    "Parameters": {
                    },
                    "Steps": [
                        {
                            "Name": "Get Data",
                            "Description": "This is a sample get data step",
                            "Sequence_Id": 1,
                            "Parameters": {
                            },
                            "Provider": "",
                            "Properties": {
                                "Stop_On_Error": True
                            },
                            "Enabled": True
                        }
                    ],
                    "Enabled": True
                },
                {
                    "Name": "Second Stage",
                    "Description": "Retrieves Sample Data from file",
                    "Sequence_Id": 2,
                    "Parameters": {
                        "Dataset": "$.Stages.FirstStage.Steps.GetData.Result"
                    },
                    "Steps": [
                        {
                            "Name": "Transform Data",
                            "Description": "",
                            "Sequence_Id": 1,
                            "Parameters": {
                                "Parameter": "a"
                            },
                            "Provider": "NullProvider",
                            "Properties": {
                                "Stop_On_Error": True
                            },
                            "Enabled": True
                        },
                        {
                            "Name": "Save Data",
                            "Description": "",
                            "Sequence_Id": 2,
                            "Parameters": {

                            },
                            "Provider": "",
                            "Properties": {
                                "Stop_On_Error": True
                            },
                            "Enabled": True
                        }
                    ],
                    "Enabled": True
                }
            ],
            "Enabled": True
        })

    def test_loads_json_in_different_positions_and_using_properties_overrides(self, json_source):
        return (exjson.loads(json_source, encoding='utf-8', includes_path="./samples"), {
            "Name": "Test Name",
            "Values": [
                {
                    "Value_id": "0AEC4D9BC52AB96E424CD057A59CC45EFF314107",
                    "Value": "test message 1"
                },
                {
                    "Value_id": "FFEB4A18FF1C37E59290C86B92DF28F65DB584D9",
                    "Value": "test message"
                }
            ],
            "Other1": {
                "Value_id": "512D4C2E2A63AC8C385A1E2315ABCF4B3D5C7A9F",
                "Value": "test message 2"
            },
            "Other2": "Test Value",
            "Other3": {
                "Value_id": "4034A54700430B6A37E56B5C38070F6B1F333B7B",
                "Value": "test message 2"
            }
        })

    def loads_json_includes_followed_by_comment_before_EOF(self, json_source):
        return (exjson.loads(json_source, encoding='utf-8'), {
            "Name": "Test",
            "Enabled": True,
            "Test1": {
                "Name": "Sample Values",
                "Enabled": True,
                "Values": [
                    "A",
                    "AB",
                    "ABC"
                ],
                "Count": 3
            },
            "Test": [
                {
                    "Name": "Sample Values",
                    "Enabled": True,
                    "Values": [
                        "A",
                        "AB",
                        "ABC"
                    ],
                    "Count": 3
                }
            ],
            "Value": {
                "Name": "Sample Values",
                "Enabled": True,
                "Values": [
                    "A",
                    "AB",
                    "ABC"
                ],
                "Count": 3
            }
        })

    def loads_json_missing_include_raises_an_error(self, json_source):
        return exjson.loads(json_source, encoding='utf-8', includes_path="./samples",
                            error_on_include_file_not_found=True)

    def loads_json_missing_include_does_not_raise_error_if_specified(self, json_source):
        return (exjson.loads(json_source, encoding='utf-8', includes_path="./samples",
                             error_on_include_file_not_found=False), {
                    "Name": "Test Name",
                    "Values": [
                        {
                            "Value_id": "FFEB4A18FF1C37E59290C86B92DF28F65DB584D9",
                            "Value": "test message"
                        }
                    ],
                    "Other1": {
                        "Value_id": "512D4C2E2A63AC8C385A1E2315ABCF4B3D5C7A9F",
                        "Value": "test message 2"
                    },
                    "Other2": "Test Value",
                    "Other3": {
                        "Value_id": "4034A54700430B6A37E56B5C38070F6B1F333B7B",
                        "Value": "test message 2"
                    }
                })

    def loads_json_with_multi_level_include(self):
        return (exjson.load("./samples/multi-level-include/multi-level-include-main.json", encoding='utf-8'), {
            "Name": "Test",
            "Value": "30l2l3l2l3l2--3lo",
            "Level1": {
                "Name": "Test 1",
                "Value1": "1",
                "Level2": {
                    "Name": "Test 2",
                    "Value1": "2",
                    "Level2": {
                        "Name": "Test 3",
                        "Value1": "3"
                    }
                }
            },
            "Level2": {
                "Name": "Test 2",
                "Value1": "2",
                "Level2": {
                    "Name": "Test 3",
                    "Value1": "3"
                }
            },
            "Level3": {
                "Name": "Test 3",
                "Value1": "3"
            }
        })

    def loads_json_with_multiple_level_recursion_detection(self):
        return exjson.load("./samples/multi-level-include/multi-level-include-recursive-first.json",
                           encoding='utf-8')

    def loads_json_without_property_override_raises_an_error(self, json_source):
        return exjson.loads(json_source, encoding='utf-8', includes_path="./samples")


class PyXJSONTests(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scenarios = EXJSONTestScenarios()

    # Load: Load JSON from file

    def test_load_simple_json(self):
        result = tests.generate_call_graph(self._scenarios.load_simple_json)
        self.assertDictEqual(result[0], result[1])

    def test_load_json_with_comments(self):
        result = tests.generate_call_graph(self._scenarios.load_json_with_comments)
        self.assertDictEqual(result[0], result[1])

    def test_load_json_with_comments_and_included_files(self):
        result = tests.generate_call_graph(self._scenarios.load_json_with_comments_and_included_files)
        self.assertDictEqual(result[0], result[1])

    def test_load_json_in_different_positions(self):
        result = tests.generate_call_graph(self._scenarios.load_json_in_different_positions)
        self.assertDictEqual(result[0], result[1])

    # Load: Load JSON from string

    def test_loads_simple_json_string(self):
        with open("./samples/clean-simple.json", encoding="utf-8") as f:
            json_source = f.read()
        result = tests.generate_call_graph(self._scenarios.loads_simple_json_string, json_source)
        self.assertDictEqual(result[0], result[1])

    def test_loads_with_includes_and_no_provided_includes_path(self):
        json_source = """{
        "Name": "Test",
        // #INCLUDE <Value:tests/samples/loads-include-test.json>
        "Enabled": true
        }
        """
        result = tests.generate_call_graph(
            self._scenarios.loads_with_includes_and_no_provided_includes_path, json_source)
        self.assertDictEqual(result[0], result[1])

    def test_loads_json_string_with_comments(self):
        with open("./samples/pipeline.stage.001.json", encoding="utf-8") as f:
            json_source = f.read()
        result = tests.generate_call_graph(self._scenarios.loads_json_string_with_comments,
                                          json_source)
        self.assertDictEqual(result[0], result[1])

    def test_loads_json_with_comments_and_included_files(self):
        with open("./samples/pipeline.json", encoding="utf-8") as f:
            json_source = f.read()
        result = tests.generate_call_graph(self._scenarios.loads_json_with_comments_and_included_files,
                                          json_source)
        self.assertDictEqual(result[0], result[1])

    def test_loads_json_in_different_positions_and_using_properties_overrides(self):
        with open("./samples/multi-include.json", encoding="utf-8") as f:
            json_source = f.read()
        result = tests.generate_call_graph(
            self._scenarios.test_loads_json_in_different_positions_and_using_properties_overrides,
            json_source)
        self.assertDictEqual(result[0], result[1])

    def test_loads_json_without_property_override_raises_an_error(self):
        with open("./samples/include-without-property.json", encoding='utf-8') as f:
            json_source = f.read()
        try:
            result = tests.generate_call_graph(
                self._scenarios.loads_json_without_property_override_raises_an_error,
                json_source)
            self.fail()
        except json.decoder.JSONDecodeError as ex:
            # 2nd Element on line 3 is invalid (missing property name)
            self.assertTrue("line 3" in str(ex))


    def test_loads_json_includes_followed_by_comment_before_EOF(self):
        json_source = """{
            // This tests that the include ignores comments
            /* #INCLUDE <Test1:tests/samples/loads-include-test.json> */
            "Name": "Test",
            "Test": [
                /* #INCLUDE <tests/samples/loads-include-test.json> */
            ],
            "Enabled": true
            // #INCLUDE <Value:tests/samples/loads-include-test.json>
            /*
            No more properties beyond here...
            */
            }
            """
        result = tests.generate_call_graph(
            self._scenarios.loads_json_includes_followed_by_comment_before_EOF, json_source)
        self.assertDictEqual(result[0], result[1])


    def test_loads_json_missing_include_raises_an_error(self):
        result = None
        with open("./samples/multi-include-with-missing-ref.json", encoding="utf-8") as f:
            json_source = f.read()
            try:
                result = tests.generate_call_graph(
                    self._scenarios.loads_json_missing_include_raises_an_error, json_source)
            except Exception as ex:
                result = ex
        self.assertIsNotNone(result)


    def test_loads_json_missing_include_does_not_raise_error_if_specified(self):
        with open("./samples/multi-include-with-missing-ref.json", encoding="utf-8") as f:
            json_source = f.read()
            try:
                result = tests.generate_call_graph(
                    self._scenarios.loads_json_missing_include_does_not_raise_error_if_specified,
                    json_source)
            except Exception as ex:
                self.fail(ex)
        self.assertDictEqual(result[0], result[1])


    # Multi-Level Include

    def test_loads_json_with_multi_level_include(self):
        result = tests.generate_call_graph(self._scenarios.loads_json_with_multi_level_include)
        self.assertDictEqual(result[0], result[1])


    def test_loads_json_with_multiple_level_recursion_detection(self):
        try:
            result = tests.generate_call_graph(
                self._scenarios.loads_json_with_multiple_level_recursion_detection)
            self.fail()
        except exjson.IncludeRecursionError as ex:
            self.assertTrue("multi-level-include-recursive-first.json" in str(ex))
