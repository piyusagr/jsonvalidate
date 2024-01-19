from typing import Union, Optional, List, Dict, Any
import json

class JsonValidator:
    """
    A class for validating JSON against a given schema.
    """

    @staticmethod
    def validate_schema(json_file: str, schema_file: str) -> bool:
        """
        Validates the JSON file against the given schema file.

        :param json_file: The path to the JSON file to be validated.
        :type json_file: str
        :param schema_file: The path to the schema file used for validation.
        :type schema_file: str
        :return: True if validation succeeds, False otherwise.
        :rtype: bool
        """
        with open(json_file, 'r') as json_data:
            data = json.load(json_data)

        with open(schema_file, 'r') as schema_data:
            schema = json.load(schema_data)

        if JsonValidator._validate_required_fields(data, schema) and \
           JsonValidator._validate_one_of_fields(data, schema) and \
           JsonValidator._validate_either_or_fields(data, schema) and \
           JsonValidator._validate_mutually_exclusive_fields(data, schema) and \
           JsonValidator._validate_enum_fields(data, schema):
            return True
        else:
            return False

    @staticmethod
    def _validate_required_fields(data: dict, schema: dict) -> bool:
        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in data:
                return False
        return True

    @staticmethod
    def _validate_one_of_fields(data: dict, schema: dict) -> bool:
        one_of_fields = schema.get('oneOf', [])
        for field_group in one_of_fields:
            present_fields = [field for field in field_group if field in data]
            if len(present_fields) > 1:
                return False
        return True

    @staticmethod
    def _validate_either_or_fields(data: dict, schema: dict) -> bool:
        either_or_fields = schema.get('eitherOr', [])
        for field_group in either_or_fields:
            present_fields = [field for field in field_group if field in data]
            if len(present_fields) > 1:
                return False
        return True
    @staticmethod
    def _validate_mutually_exclusive_fields(data: dict, schema: dict) -> bool:
        mutually_exclusive_fields = schema.get('mutuallyExclusive', [])
        for field_group in mutually_exclusive_fields:
            present_fields = [field for field in field_group if field in data]
            if len(present_fields) > 1:
                return False
        return True

    @staticmethod
    def _validate_enum_fields(data: dict, schema: dict) -> bool:
        enum_fields = schema.get('enum', {})
        for field, allowed_values in enum_fields.items():
            if field in data and data[field] not in allowed_values:
                return False
        return True


class DataDogMetricsSender:
    """
    A class for sending metrics to DataDog.
    """

    @staticmethod
    def send_metric(
        metric_name: str,
        datapoint: Union[float, int],
        tags: Optional[List[str]] = None,
        type_: Optional[str] = None,
        interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Sends a single datapoint metric to DataDog.

        :param metric_name: The name of the metric.
        :type metric_name: str
        :param datapoint: A single integer or float related to the metric.
        :type datapoint: int or float
        :param tags: A list of tags associated with the metric.
        :type tags: list
        :param type_: Type of your metric: gauge, rate, or count.
        :type type_: str
        :param interval: If the type of the metric is rate or count, define the corresponding interval.
        :type interval: int
        :return: A dictionary containing information about the sent metric.
        :rtype: dict
        """
        # Actual implementation of sending metric to DataDog goes here
        metric_info = {
            'metric_name': metric_name,
            'datapoint': datapoint,
            'tags': tags,
            'type': type_,
            'interval': interval
        }
     

        return metric_info

# Example usage:
json_validator = JsonValidator()

# Example JSON data and schema file paths
json_file_path = 'D:\jsonvalidate\person.json'
schema_file_path = 'D:\jsonvalidate\person_schema.json'

# Validate JSON against schema
if json_validator.validate_schema(json_file_path, schema_file_path):
    # JSON is valid, proceed to send metric
    print("JSON validateed successfully!!")
    datadog_sender = DataDogMetricsSender()
    result = datadog_sender.send_metric(
        metric_name='example_metric',
        datapoint=42,
        tags=['tag1', 'tag2'],
        type_='gauge',
        interval=60
    )
    print("metric sent: ",result)
else:
    print("JSON validation failed.")
