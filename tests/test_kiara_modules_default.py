#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kiara.documentation` package."""

import pytest  # noqa

import kiara_plugin.documentation


def test_assert():

    assert kiara_plugin.documentation.get_version() is not None
