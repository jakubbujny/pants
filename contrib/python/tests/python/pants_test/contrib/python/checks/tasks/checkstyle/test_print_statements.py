# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from future.utils import PY3
from pants_test.contrib.python.checks.tasks.checkstyle.plugin_test_base import \
  CheckstylePluginTestBase

from pants.contrib.python.checks.tasks.checkstyle.print_statements import PrintStatements


class PrintStatementsTest(CheckstylePluginTestBase):
  plugin_type = PrintStatements

  def test_print_override(self):
    statement = """
      from __future__ import print_function
      print("I do what I want")

      class Foo(object):
        def print(self):
          "I can do this because it's not a reserved word."
    """
    self.assertNoNits(statement)

  def test_print_function(self):
    statement = """
      print("I do what I want")
    """
    self.assertNoNits(statement)

  @pytest.mark.skipif(PY3, reason='Print statement check disabled on Python 3 because interpreter will already '
                                  'throw a syntax error.')
  def test_print_statement(self):
    statement = """
      print["I do what I want"]
    """
    self.assertNit(statement, 'T607')
