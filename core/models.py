from typing import Any, Dict

from bson.objectid import ObjectId

from pydantic_core import CoreSchema

from pydantic import GetJsonSchemaHandler


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls) -> ObjectId:
        yield cls.validate

    @classmethod
    def validate(cls, v) -> ObjectId:
        try:
            return ObjectId(str(v))
        except Exception:
            raise ValueError("Not a valid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> Dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type="string")
        return json_schema
