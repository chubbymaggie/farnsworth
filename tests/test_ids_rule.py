#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import os
import time

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeSet, IDSRule, Round, Team

NOW = datetime.now()


class TestIDSRule:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_submit(self):
        Round.create(num=0, ends_at=NOW + timedelta(seconds=30))
        Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        ids = IDSRule.create(cs=cs, rules="aaa", sha256="bbb")

        assert_equals(len(ids.fieldings), 0)
        ids.submit()
        assert_equals(len(ids.fieldings), 1)
        assert_equals(ids.fieldings.get().team, Team.get_our())
        assert_equals(ids.fieldings.get().submission_round, Round.current_round())

    def test_generate_hash_on_create_and_save_if_missing(self):
        cs = ChallengeSet.create(name="foo")

        ids_create = IDSRule.create(cs=cs, rules="aaa")
        assert_equals(ids_create.sha256, "9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0")

        ids_save = IDSRule(cs=cs, rules="bbb")
        ids_save.save()
        assert_equals(ids_save.sha256, "3e744b9dc39389baf0c5a0660589b8402f3dbb49b89b3e75f2c9355852a3c677")

        ids_set = IDSRule.create(cs=cs, rules="ccc", sha256="ddd")
        assert_equals(ids_set.sha256, "ddd")
