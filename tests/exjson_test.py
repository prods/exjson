from unittest import TestCase

import exjson

__author__ = 'Pedro Rodriguez'
__project__ = 'xjson'


class PyXJSONTests(TestCase):

    def test_loading_simple_json(self):
        simple_json = exjson.loads("./samples/clean-simple.json")
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
        simple_json = exjson.loads("./samples/pipeline.stage.001.json", encoding='utf-8')
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
        simple_json = exjson.loads("./samples/pipeline.json", encoding='utf-8')
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
        json_content = exjson.loads("./samples/multi-include.json", encoding='utf-8')
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
