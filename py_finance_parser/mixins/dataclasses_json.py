from dataclasses_json import DataClassJsonMixin


class ListDataClassJsonMixin(DataClassJsonMixin):
    @classmethod
    def list_to_json(cls, list_of_objects: list) -> str:
        """Serializes a list of objects that are instances of this class into a json string

        Args:
            list_of_objects (list): the list of objects to serialize

        Returns:
            str: the json string
        """
        return cls().schema().dumps(list_of_objects, many=True)

    @classmethod
    def json_to_list(cls, json_string: str) -> list:
        """Deserializes a json string into a list of instances of this class

        Args:
            json_string (str): the json string to deserialize into a list

        Returns:
            list: the deserialized list of dataclass objects from the json string
        """
        cls.schema().loads(json_string, many=True)
