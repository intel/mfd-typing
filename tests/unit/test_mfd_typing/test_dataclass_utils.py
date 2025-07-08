# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, fields

from mfd_typing.dataclass_utils import get_field_type, convert_value_field_to_typehint_type


@dataclass
class TestClass:
    field1: int
    field2: str
    field3: str | None = None
    field4: None | int = None


class TestDataclassUtils:
    def test_get_field_type(self):
        assert issubclass(get_field_type(TestClass.__dataclass_fields__["field1"]), int)
        assert issubclass(get_field_type(TestClass.__dataclass_fields__["field2"]), str)
        assert issubclass(get_field_type(TestClass.__dataclass_fields__["field3"]), str)
        assert issubclass(get_field_type(TestClass.__dataclass_fields__["field4"]), int)

    def test_convert_value_field_to_typehint_type(self):
        obj = TestClass(field1=1.123, field2=1.123, field3=1.123, field4=1.123)

        for f in fields(obj):
            convert_value_field_to_typehint_type(obj, f)

        assert isinstance(obj.field1, int)
        assert isinstance(obj.field2, str)
        assert isinstance(obj.field3, str)
        assert isinstance(obj.field4, int)
