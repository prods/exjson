from unittest import TestCase

import exjson

__author__ = 'Pedro Rodriguez'
__project__ = 'xjson'


class PyXJSONTests(TestCase):

    # Load: Load JSON from file

    def test_load_simple_json(self):
        simple_json = exjson.load("./samples/clean-simple.json")
        self.assertDictEqual(simple_json, {
            "Name": "Sample Values",
            "Enabled": True,
            "Values": [
                "A",
                "AB",
                "ABC"
            ],
            "Count": 3
        })

    def test_load_json_with_comments(self):
        simple_json = exjson.load("./samples/pipeline.stage.001.json", encoding='utf-8')
        self.assertDictEqual(simple_json, {
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

    def test_load_json_with_comments_and_included_files(self):
        simple_json = exjson.load("./samples/pipeline.json", encoding='utf-8')
        self.assertDictEqual(simple_json, {
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

    def test_load_json_in_different_positions(self):
        json_content = exjson.load("./samples/multi-include.json", encoding='utf-8')
        self.assertDictEqual(json_content, {
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

    # Load: Load JSON from string

    def test_loads_simple_json_string(self):
        with open("./samples/clean-simple.json", encoding="utf-8") as f:
            json_source = f.read()
        simple_json = exjson.loads(json_source, encoding='utf-8')
        self.assertDictEqual(simple_json, {
            "Name": "Sample Values",
            "Enabled": True,
            "Values": [
                "A",
                "AB",
                "ABC"
            ],
            "Count": 3
        })

    def test_loads_with_includes_and_no_provided_includes_path(self):
        json_source = """{
        "Name": "Test",
        // #INCLUDE <Value:tests/samples/loads-include-test.json>
        "Enabled": true
        }
        """
        simple_json = exjson.loads(json_source, encoding='utf-8')
        self.assertDictEqual(simple_json, {
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

    def test_loads_json_string_with_comments(self):
        with open("./samples/pipeline.stage.001.json", encoding="utf-8") as f:
            json_source = f.read()
        simple_json = exjson.loads(json_source, encoding='utf-8')
        self.assertDictEqual(simple_json, {
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

    def test_loads_json_with_comments_and_included_files(self):
        with open("./samples/pipeline.json", encoding="utf-8") as f:
            json_source = f.read()
        simple_json = exjson.loads(json_source, encoding='utf-8', includes_path="./samples")
        self.assertDictEqual(simple_json, {
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

    def test_loads_json_in_different_positions(self):
        with open("./samples/multi-include.json", encoding="utf-8") as f:
            json_source = f.read()
        json_content = exjson.loads(json_source, encoding='utf-8', includes_path="./samples")
        self.assertDictEqual(json_content, {
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
        simple_json = exjson.loads(json_source, encoding='utf-8')
        self.assertDictEqual(simple_json, {
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

    def test_loads_json_missing_include_raises_an_error(self):
        result = None
        with open("./samples/multi-include-with-missing-ref.json", encoding="utf-8") as f:
            json_source = f.read()
            try:
                json_content = exjson.loads(json_source, encoding='utf-8', includes_path="./samples",
                                            error_on_include_file_not_found=True)
            except Exception as ex:
                result = ex
        self.assertIsNotNone(result)

    def test_loads_json_missing_include_does_not_raise_error_if_specified(self):
        result = None
        with open("./samples/multi-include-with-missing-ref.json", encoding="utf-8") as f:
            json_source = f.read()
            try:
                json_content = exjson.loads(json_source, encoding='utf-8', includes_path="./samples",
                                            error_on_include_file_not_found=False)
            except Exception as ex:
                self.fail(ex)
        self.assertDictEqual(json_content, {
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

    # Multi-Level Include

    def test_loads_json_with_four_level_include(self):
        simple_json = exjson.load("./samples/multi-level-include/multi-level-include-main.json", encoding='utf-8')
        self.assertDictEqual(simple_json, {
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

    def test_loads_json_with_multiple_level_recursion_detection(self):
        self.assertIsNotNone(None)