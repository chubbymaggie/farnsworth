#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""patch_scores model"""

from __future__ import absolute_import, unicode_literals

from peewee import BooleanField, ForeignKeyField, BigIntegerField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .round import Round
from .challenge_set import ChallengeSet
from ..mixins.cb_score_mixin import CBScoreMixin
from .patch_type import PatchType


class PatchScore(BaseModel, CBScoreMixin):
    """
    Score of a patched CB
    """
    cs = ForeignKeyField(ChallengeSet, related_name='patch_scores')
    num_polls = BigIntegerField(null=False)
    polls_included = BinaryJSONField(null=True)
    has_failed_polls = BooleanField(null=False, default=False)
    failed_polls = BinaryJSONField(null=True)
    round = ForeignKeyField(Round, related_name='patch_scores')
    perf_score = BinaryJSONField(null=False)
    patch_type = ForeignKeyField(PatchType, related_name='estimated_scores')

    @property
    def security(self):
        return 2 - self.patch_type.exploitability

    @property
    def success(self):
        if self.has_failed_polls:
            return 0
        else:
            return 1 - self.patch_type.functionality_risk

    @property
    def time_overhead(self):
        rep_tsk_clk = self.perf_score['score']['rep']['task_clock']
        ref_tsk_clk = self.perf_score['score']['ref']['task_clock']
        exec_time_overhead = 9999  # big number
        if ref_tsk_clk != 0:
            exec_time_overhead = (rep_tsk_clk * 1.0) / ref_tsk_clk
        return exec_time_overhead - 1

    @property
    def memory_overhead(self):
        rep_max_rss = self.perf_score['score']['rep']['rss']
        ref_max_rss = self.perf_score['score']['ref']['rss']
        rep_min_flt = self.perf_score['score']['rep']['flt']
        ref_min_flt = self.perf_score['score']['ref']['flt']

        term1 = 9999  # big number
        if ref_max_rss != 0:
            term1 = (rep_max_rss * 1.0) / ref_max_rss

        term2 = 9999  # big number
        if ref_min_flt != 0:
            term2 = (rep_min_flt * 1.0) / ref_min_flt
        return 0.5 * (term1 + term2) - 1

    @property
    def size_overhead(self):
        # ref performance : Un patched
        # rep performance : patched
        rep_file_size = self.perf_score['score']['rep']['file_size']
        ref_file_size = self.perf_score['score']['ref']['file_size']
        return ((rep_file_size * 1.0) / ref_file_size) - 1
