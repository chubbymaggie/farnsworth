"""IDSRuleFielding model"""

import os
from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .ids_rule import IDSRule
from .round import Round
from .team import Team

class IDSRuleFielding(BaseModel):
    """IDSRuleFielding model"""

    ids_rule = ForeignKeyField(IDSRule, db_column='ids_rule_id', to_field='id',
                               related_name='fieldings', null=False)
    team = ForeignKeyField(Team, db_column='team_id', to_field='id',
                           related_name='fieldings', null=False)
    submission_round = ForeignKeyField(Round, db_column='submission_round_id',
                                       to_field='id', related_name='fieldings', null=False)
    available_round = ForeignKeyField(Round, db_column='available_round_id',
                                      to_field='id', related_name='fieldings', null=True)
    fielded_round = ForeignKeyField(Round, db_column='fielded_round_id',
                                    to_field='id', related_name='fieldings', null=True)
