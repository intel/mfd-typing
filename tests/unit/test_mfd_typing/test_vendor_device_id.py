# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
import collections

import pytest

from mfd_typing.vendor_device_id import VendorID, DeviceID, SubVendorID, SubDeviceID, _VendorDeviceID


class TestVendorDeviceID:
    cls = _VendorDeviceID

    def test_hashable(self):
        assert isinstance(self.cls(0xDEAD), collections.abc.Hashable)
        assert hash(self.cls(0xDEAD)) == hash(0xDEAD)

    @pytest.mark.parametrize("value", [-1, 0xFFFF + 1])
    def test_input_out_of_range(self, value):
        with pytest.raises(ValueError):
            self.cls(value)

    def test_input_incorrect_type(self, mocker):
        with pytest.raises(TypeError):
            self.cls(mocker.sentinel.input)

    def test_input_incorrect_string(self):
        with pytest.raises(ValueError):
            self.cls("foobar")

    def test_input_none(self):
        with pytest.raises(TypeError):
            self.cls(None)

    def test_defined_str(self):
        assert str(self.cls("DEAD")) == str(self.cls(0xDEAD)) == "DEAD"

    def test_defined_repr(self):
        assert repr(self.cls("DEAD")) == repr(self.cls(0xDEAD)) == f"{self.cls.__name__}('DEAD')"

    def test_incomplete_str(self):
        assert str(self.cls("AD")) == str(self.cls(0xAD)) == "00AD"

    def test_idempotent_constructor(self):
        a = self.cls(0x8086)
        assert self.cls(a) is a

    def test_equality(self):
        a = self.cls(0x8086)
        assert a == self.cls(0x8086)
        assert not a == self.cls(0x8087)

    def test_inequality(self):
        a = self.cls(0x8086)
        assert a != self.cls(0x8087)
        assert not a != self.cls(0x8086)

    def test_incomparable_to_base_types(self):
        assert self.cls(0xDEAD) != 0xDEAD
        assert self.cls(0xDEAD) != "DEAD"

    def test_cast_to_int(self):
        assert int(self.cls(0xDEAD)) == 0xDEAD


class _VendorDeviceIDDescendantMixin:
    """Mixin for testing descendants of _VendorDeviceID class."""

    cls = None
    assertNotEqual = None

    def test_incomparable_to_other_id_types(self):
        all_id_classes = [VendorID, DeviceID, SubVendorID, SubDeviceID]
        all_id_classes.remove(self.cls)

        for other_id_class in all_id_classes:
            assert self.cls(0xDEAD) != other_id_class(0xDEAD)


# By inheriting from the unit test class and changing the cls parameter we make
# sure all tests are run for all the descendant classes of _VendorDeviceID plus
# test cases from mixin
class TestVendorID(TestVendorDeviceID, _VendorDeviceIDDescendantMixin):
    cls = VendorID


class TestDeviceID(TestVendorDeviceID, _VendorDeviceIDDescendantMixin):
    cls = DeviceID


class TestSubVendorID(TestVendorDeviceID, _VendorDeviceIDDescendantMixin):
    cls = SubVendorID


class TestSubDeviceID(TestVendorDeviceID, _VendorDeviceIDDescendantMixin):
    cls = SubDeviceID
