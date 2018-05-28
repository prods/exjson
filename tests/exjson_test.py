from http import server
import json
import re
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler
from unittest import TestCase
from dateutil.tz import tzlocal

import tests
import exjson

__author__ = 'prods'
__project__ = 'exjson'


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

    def loads_json_include_default_value(self):
        return (exjson.loads("""{
            "Name": "First Stage",
            "Description": "Retrieves Sample Data from file",
            "Sequence_Id": 1,
            "Parameters": {
            },
            /* #INCLUDE <Steps:step_not_found.json|[]> */
            "Enabled": true
        }
        """, encoding='utf-8'), {
            "Name": "First Stage",
            "Description": "Retrieves Sample Data from file",
            "Sequence_Id": 1,
            "Parameters": {
            },
            "Steps": [],
            "Enabled": True
        })

    def loads_json_include_from_http_url(self):
        return (exjson.loads("""{
            "Name": "First Stage",
            "Description": "Retrieves Sample Data from file",
            "Sequence_Id": 1,
            /* #INCLUDE <Post:https://jsonplaceholder.typicode.com/posts/1|{}> */
            "Enabled": true
        }
        """, encoding='utf-8'), {
            "Name": "First Stage",
            "Description": "Retrieves Sample Data from file",
            "Sequence_Id": 1,
            "Post": {
              "userId": 1,
              "id": 1,
              "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
              "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
            },
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

    def loads_json_evaluate(self, json_source, test_name=None):
        return exjson.loads(json_source, encoding='utf-8', includes_path="./samples")

    def loads_json_evaluate_raw_date_value(self, json_source, test_name=None):
        return (exjson.loads(json_source, encoding='utf-8', includes_path="./samples"), {
            "date": datetime.now(tzlocal()).isoformat()
        })


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

    def test_loads_json_include_default_value(self):
        result = tests.generate_call_graph(self._scenarios.loads_json_include_default_value)
        self.assertDictEqual(result[0], result[1])

    def test_loads_json_include_from_http_url(self):
        result = tests.generate_call_graph(self._scenarios.loads_json_include_from_http_url)
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

    # Dynamic and Reference Value Evaluation

    def test_loads_json_evaluate_uuid_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
            "hash": "$.uuid()"
            }""", "uuid")
        self.assertIsNotNone(result["hash"], "uuid")

    def test_loads_json_evaluate_md5_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
            "hash": "$.md5()"
            }""", "md5")
        self.assertIsNotNone(result["hash"])

    def test_loads_json_evaluate_md5_of_string_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
               "hash": "$.md5('test string')"
               }""", "md5_of_string_value")
        self.assertTrue(result["hash"] == '6f8db599de986fab7a21625b7916589c')

    def test_loads_json_evaluate_sha1_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
             "hash": "$.sha1()"
             }""", "sha1")
        self.assertIsNotNone(result["hash"])

    def test_loads_json_evaluate_sha256_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
             "hash": "$.sha256()"
             }""", "sha256")
        self.assertIsNotNone(result["hash"])

    def test_loads_json_evaluate_sha512_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
             "hash": "$.sha512()"
             }""", "sha512")
        self.assertIsNotNone(result["hash"])

    def test_loads_json_evaluate_raw_date_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate_raw_date_value, """{
            "date": "$.now()"
            }""")
        iso8601 = re.compile(
            r'^(?P<full>((?P<year>\d{4})([/-]?(?P<month>(0[1-9])|(1[012]))([/-]?(?P<day>(0[1-9])|([12]\d)|(3[01])))?)?(?:T(?P<hour>([01][0-9])|(?:2[0123]))(\:?(?P<min>[0-5][0-9])(\:?(?P<sec>[0-5][0-9]([\,\.]\d{1,10})?))?)?(?:Z|([\-+](?:([01][0-9])|(?:2[0123]))(\:?(?:[0-5][0-9]))?))?)?))$')
        result_format_match = iso8601.match(result[0]["date"])
        print(result[0]["date"])

        tz_offset_hours = str(datetime.now(tzlocal()).utcoffset().total_seconds() / 3600)
        tz_offset_hours_sep = tz_offset_hours.find('.')
        tz_formatted = f"{tz_offset_hours[0]}{tz_offset_hours[1:tz_offset_hours_sep].zfill(2)}:{tz_offset_hours[tz_offset_hours_sep+1:].zfill(2)}"

        self.assertTrue(result_format_match["year"] == str(datetime.now().year) and
                        result_format_match["month"] == str(datetime.now().month).rjust(2, '0') and
                        result_format_match["day"] == str(datetime.now().day).rjust(2, '0') and
                        result_format_match["hour"] == str(datetime.now().hour).rjust(2, '0') and
                        result_format_match["min"] == str(datetime.now().minute).rjust(2, '0') and
                        result_format_match["sec"] is not None and
                        result[0]["date"].endswith(tz_formatted))

    def test_loads_json_evaluate_raw_utc_date_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate_raw_date_value, """{
            "date": "$.now().utc()"
            }""")
        iso8601 = re.compile(
            r'^(?P<full>((?P<year>\d{4})([/-]?(?P<month>(0[1-9])|(1[012]))([/-]?(?P<day>(0[1-9])|([12]\d)|(3[01])))?)?(?:T(?P<hour>([01][0-9])|(?:2[0123]))(\:?(?P<min>[0-5][0-9])(\:?(?P<sec>[0-5][0-9]([\,\.]\d{1,10})?))?)?(?:Z|([\-+](?:([01][0-9])|(?:2[0123]))(\:?(?:[0-5][0-9]))?))?)?))$')
        result_format_match = iso8601.match(result[0]["date"])
        print(result[0]["date"])
        self.assertTrue(result_format_match["year"] == str(datetime.utcnow().year) and
                        result_format_match["month"] == str(datetime.utcnow().month).rjust(2, '0') and
                        result_format_match["day"] == str(datetime.utcnow().day).rjust(2, '0') and
                        result_format_match["hour"] == str(datetime.utcnow().hour).rjust(2, '0') and
                        result_format_match["min"] == str(datetime.utcnow().minute).rjust(2, '0') and
                        result_format_match["sec"] is not None and
                        result[0]["date"].endswith("-00:00"))

    def test_loads_json_evaluate_python_formatted_now_add_date_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate_raw_date_value, """{
                    "date": "$.now('yyyy-MM-dd HH:mm')"
                    }""", "formatted_now_add_date_value")
        v = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.assertTrue(result[0]["date"] == v)

    def test_loads_json_evaluate_python_formatted_date_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate_raw_date_value, """{
                    "date": "$.now().add(days=1,'yyyy-MM-dd HH:mm')"
                    }""", "formatted")
        v = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.assertTrue(result[0]["date"] == v)

    def test_loads_json_evaluate_raw_date_value(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate_raw_date_value, """{
            "date": "$.now()"
            }""")
        iso8601 = re.compile(
            r'^(?P<full>((?P<year>\d{4})([/-]?(?P<month>(0[1-9])|(1[012]))([/-]?(?P<day>(0[1-9])|([12]\d)|(3[01])))?)?(?:T(?P<hour>([01][0-9])|(?:2[0123]))(\:?(?P<min>[0-5][0-9])(\:?(?P<sec>[0-5][0-9]([\,\.]\d{1,10})?))?)?(?:Z|([\-+](?:([01][0-9])|(?:2[0123]))(\:?(?:[0-5][0-9]))?))?)?))$')
        result_format_match = iso8601.match(result[0]["date"])
        print(result[0]["date"])

        tz_offset_hours = str(datetime.now(tzlocal()).utcoffset().total_seconds() / 3600)
        tz_offset_hours_sep = tz_offset_hours.find('.')
        tz_formatted = f"{tz_offset_hours[0]}{tz_offset_hours[1:tz_offset_hours_sep].zfill(2)}:{tz_offset_hours[tz_offset_hours_sep+1:].zfill(2)}"

        self.assertTrue(result_format_match["year"] == str(datetime.now().year) and
                        result_format_match["month"] == str(datetime.now().month).rjust(2, '0') and
                        result_format_match["day"] == str(datetime.now().day).rjust(2, '0') and
                        result_format_match["hour"] == str(datetime.now().hour).rjust(2, '0') and
                        result_format_match["min"] == str(datetime.now().minute).rjust(2, '0') and
                        result_format_match["sec"] is not None and
                        result[0]["date"].endswith(tz_formatted))


    def test_load_json_evaluate_sequence_single_int(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                            "first": [
                                { "id": $.sequence('A') },
                                { "id": $.sequence('A') },
                                { "id": $.sequence('A') },
                                { "id": $.sequence('A') }
                            ]
                            }""", "sequence_single_int")
        self.assertDictEqual(result, {
            "first": [
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4}
            ]
        })

    def test_load_json_evaluate_sequence_single_int_with_padding(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                               "first": [
                                   { "id": "$.sequence('A','{0:0>4}')" },
                                   { "id": "$.sequence('A','{0:0>4}')" },
                                   { "id": "$.sequence('A','{0:0>4}')" },
                                   { "id": "$.sequence('A','{0:0>4}')" }
                               ],
                               "second": "$.sequence('B')"
                               }""", "sequence_single_int_with_padding")
        self.assertDictEqual(result, {
            "first": [
                {"id": "0001"},
                {"id": "0002"},
                {"id": "0003"},
                {"id": "0004"}
            ],
            "second": "1"
        })

    def test_load_json_evaluate_sequence_single_int_with_steps(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                               "first": [
                                   { "id": "$.sequence('A', null, 2)" },
                                   { "id": "$.sequence('A', null, 2)" },
                                   { "id": "$.sequence('A', null, 2)" },
                                   { "id": "$.sequence('A', null, 2)" }
                               ],
                               "second": "$.sequence('B')"
                               }""", "sequence_single_int_with_steps")
        self.assertDictEqual(result, {
            "first": [
                {"id": "2"},
                {"id": "4"},
                {"id": "6"},
                {"id": "8"}
            ],
            "second": "1"
        })

    def test_load_json_evaluate_sequence_multiple_int(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                            "first": [
                                { "id": $.sequence('A') },
                                { "id": $.sequence('A') },
                                { "id": $.sequence('A') },
                                { "id": $.sequence('A') }
                            ],
                            "second": [
                                { "id": $.sequence('B') },
                                { "id": $.sequence('B') },
                                { "id": $.sequence('B') },
                                { "id": $.sequence('B') }
                            ],
                            "third": [
                                { "id": $.sequence('A') }
                            ]
                            }""", "sequence_multiple_int")
        self.assertDictEqual(result, {
            "first": [
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4}
            ],
            "second": [
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4}
            ],
            "third": [
                {"id": 5}
            ]
        })

    def test_loads_json_evaluate_sequence_multiple_string(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                            "first": [
                                { "id": "AX-$.sequence('A')" },
                                { "id": "AX-$.sequence('A')" },
                                { "id": "AX-$.sequence('A')" },
                                { "id": "AX-$.sequence('A')" }
                            ],
                            "second": [
                                { "id": "BX-$.sequence('B')" },
                                { "id": "BX-$.sequence('B')" },
                                { "id": "BX-$.sequence('B')" },
                                { "id": "BX-$.sequence('B')" }
                            ],
                            "third": [
                                { "id": "AXX-$.sequence('A')" }
                            ]
                            }""", "sequence_multiple_string")
        self.assertDictEqual(result, {
            "first": [
                {"id": "AX-1"},
                {"id": "AX-2"},
                {"id": "AX-3"},
                {"id": "AX-4"}
            ],
            "second": [
                {"id": "BX-1"},
                {"id": "BX-2"},
                {"id": "BX-3"},
                {"id": "BX-4"}
            ],
            "third": [
                {"id": "AXX-5"}
            ]
        })

    def test_loads_json_evaluate_register_custom_extension_function(self):
        def custom_add(*args):
            result = 0
            for r in args:
                result = result + int(r)
            return result
        exjson.register_custom_scripting_extension("test", custom_add)
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                "a": "$.test(10, 20)"
            }""", "register_custom_extension_function")
        self.assertDictEqual(result, {
                "a": "30"
            })

    def test_load_json_evaluate_root_references(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                            "prefix": "A",
                            "first": [
                                { "id": "A1" },
                                { "id": "A2" },
                                { "id": "A3" },
                                { "id": "$root.prefix4" }
                            ],
                            "second": "$root.prefix",
                            "third": {
                                "test1": 23,
                                "test2": [
                                    1,2,3
                                ],
                                "test3": {
                                    "deep1": 44,
                                    "deep2": false,
                                    "deep3": "$root.second",
                                    "deep4": "$root.third.test1"
                                }
                            }
                            }""", "root_references")
        self.assertDictEqual(result, {
            "prefix": "A",
            "first": [
                {"id": "A1"},
                {"id": "A2"},
                {"id": "A3"},
                {"id": "A4"}
            ],
            "second": "A",
            "third": {
                "test1": 23,
                "test2": [
                    1, 2, 3
                ],
                "test3": {
                    "deep1": 44,
                    "deep2": False,
                    "deep3": "A",
                    "deep4": "23"
                }
            }
        })

    def test_load_json_evaluate_parent_references(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                            "prefix": "A",
                            "first": [
                                { "id": "A1" },
                                { "id": "A2" },
                                { "id": "A3" },
                                { "id": "$root.prefix4" }
                            ],
                            "second": "$root.prefix",
                            "third": {
                                "test1": 23,
                                "test2": [
                                    1,2,3
                                ],
                                "test3": {
                                    "deep1": 44,
                                    "deep2": false,
                                    "deep3": "$root.secondB",
                                    "deep4": "AZ-$parent.test1X"
                                }
                            }
                            }""", "parent_references")
        self.assertDictEqual(result, {
            "prefix": "A",
            "first": [
                {"id": "A1"},
                {"id": "A2"},
                {"id": "A3"},
                {"id": "A4"}
            ],
            "second": "A",
            "third": {
                "test1": 23,
                "test2": [
                    1, 2, 3
                ],
                "test3": {
                    "deep1": 44,
                    "deep2": False,
                    "deep3": "AB",
                    "deep4": "AZ-23X"
                }
            }
        })

    def test_load_json_evaluate_this_references(self):
        result = tests.generate_call_graph(
            self._scenarios.loads_json_evaluate, """{
                            "prefix": "A",
                            "first": [
                                { "id": "A1" },
                                { "id": "A2" },
                                { "id": "A3" },
                                { "id": "$root.prefix4" }
                            ],
                            "second": "$root.prefix",
                            "third": {
                                "test1": 23,
                                "test2": [
                                    1,2,3
                                ],
                                "test3": {
                                    "deep1": 44,
                                    "deep2": false,
                                    "deep3": "$root.second",
                                    "deep4": $this.deep1
                                }
                            }
                            }""", "this_references")
        self.assertDictEqual(result, {
            "prefix": "A",
            "first": [
                {"id": "A1"},
                {"id": "A2"},
                {"id": "A3"},
                {"id": "A4"}
            ],
            "second": "A",
            "third": {
                "test1": 23,
                "test2": [
                    1, 2, 3
                ],
                "test3": {
                    "deep1": 44,
                    "deep2": False,
                    "deep3": "A",
                    "deep4": 44
                }
            }
        })

