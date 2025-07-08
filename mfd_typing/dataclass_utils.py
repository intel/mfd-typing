# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for dataclass typing helpers."""

from typing import ForwardRef, Union, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dataclasses import Field


def get_field_type(field: "Field") -> Union[type, str]:
    """
    Get type hint of given field of given model.

    If type hint is a Union - return first not None-type type.
    In case of ForwardRef (type hint declared as str, not as type) return str.

    :param field: Field to get type from.
    :return: Type of field.
    """
    if isinstance(field.type, type) or isinstance(field.type, str):
        return field.type

    for type_hint in field.type.__args__:
        if isinstance(type_hint, ForwardRef):
            return type_hint.__forward_arg__
        elif not issubclass(type_hint, type(None)):
            return type_hint

    raise TypeError("Not found proper type hint.")


def convert_value_field_to_typehint_type(obj: Any, field: "Field") -> None:
    """
    Convert value of dataclass field to type expected in typehints for this field.

    :param obj: self objects of dataclass
    :param field: field of dataclass iterated from fields(self) function
    """
    value = getattr(obj, field.name)
    if value is None:
        return

    try:
        field_type = get_field_type(field)
        if not isinstance(value, field_type):
            # force reset arguments on frozen dataclass
            obj.__dict__[field.name] = field_type(value)
    except TypeError:
        pass
