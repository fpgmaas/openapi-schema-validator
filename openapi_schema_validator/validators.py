import warnings
from typing import Any
from typing import Type

from jsonschema import _legacy_validators
from jsonschema import _validators
from jsonschema.validators import Draft202012Validator
from jsonschema.validators import create
from jsonschema.validators import extend
from jsonschema_specifications import REGISTRY as SPECIFICATIONS

from openapi_schema_validator import _format as oas_format
from openapi_schema_validator import _types as oas_types
from openapi_schema_validator import _validators as oas_validators
from openapi_schema_validator._types import oas31_type_checker

OAS30Validator = create(
    meta_schema=SPECIFICATIONS.contents(
        "http://json-schema.org/draft-04/schema#",
    ),
    validators={
        "multipleOf": _validators.multipleOf,
        # exclusiveMaximum supported inside maximum_draft3_draft4
        "maximum": _legacy_validators.maximum_draft3_draft4,
        # exclusiveMinimum supported inside minimum_draft3_draft4
        "minimum": _legacy_validators.minimum_draft3_draft4,
        "maxLength": _validators.maxLength,
        "minLength": _validators.minLength,
        "pattern": _validators.pattern,
        "maxItems": _validators.maxItems,
        "minItems": _validators.minItems,
        "uniqueItems": _validators.uniqueItems,
        "maxProperties": _validators.maxProperties,
        "minProperties": _validators.minProperties,
        "enum": _validators.enum,
        # adjusted to OAS
        "type": oas_validators.type,
        "allOf": oas_validators.allOf,
        "oneOf": oas_validators.oneOf,
        "anyOf": oas_validators.anyOf,
        "not": _validators.not_,
        "items": oas_validators.items,
        "properties": _validators.properties,
        "required": oas_validators.required,
        "additionalProperties": oas_validators.additionalProperties,
        # TODO: adjust description
        "format": oas_validators.format,
        # TODO: adjust default
        "$ref": _validators.ref,
        # fixed OAS fields
        "discriminator": oas_validators.not_implemented,
        "readOnly": oas_validators.readOnly,
        "writeOnly": oas_validators.writeOnly,
        "xml": oas_validators.not_implemented,
        "externalDocs": oas_validators.not_implemented,
        "example": oas_validators.not_implemented,
        "deprecated": oas_validators.not_implemented,
    },
    type_checker=oas_types.oas30_type_checker,
    format_checker=oas_format.oas30_format_checker,
    # NOTE: version causes conflict with global jsonschema validator
    # See https://github.com/python-openapi/openapi-schema-validator/pull/12
    # version="oas30",
    id_of=lambda schema: schema.get("id", ""),
)

OAS30ReadValidator = extend(
    OAS30Validator,
    validators={
        "required": oas_validators.read_required,
        "readOnly": oas_validators.not_implemented,
        "writeOnly": oas_validators.writeOnly,
    },
)
OAS30WriteValidator = extend(
    OAS30Validator,
    validators={
        "required": oas_validators.write_required,
        "readOnly": oas_validators.readOnly,
        "writeOnly": oas_validators.not_implemented,
    },
)

OAS31Validator = extend(
    Draft202012Validator,
    {
        # adjusted to OAS
        "allOf": oas_validators.allOf,
        "oneOf": oas_validators.oneOf,
        "anyOf": oas_validators.anyOf,
        "description": oas_validators.not_implemented,
        # fixed OAS fields
        "discriminator": oas_validators.not_implemented,
        "xml": oas_validators.not_implemented,
        "externalDocs": oas_validators.not_implemented,
        "example": oas_validators.not_implemented,
    },
    type_checker=oas31_type_checker,
    format_checker=oas_format.oas31_format_checker,
)
