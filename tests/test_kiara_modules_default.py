#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kiara_documentation` package."""

import pytest  # noqa

import kiara_documentation


def test_assert():

    assert kiara_documentation.get_version() is not None
