#  Copyright 2022 Red Hat, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sqlalchemy as sa
from sqlalchemy.sql import func

from .base import metadata

__all__ = (
    "projects",
    "inventories",
    "extra_vars",
    "playbooks",
)

projects = sa.Table(
    "project",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        sa.Identity(always=True),
        primary_key=True,
    ),
    sa.Column("git_hash", sa.String),
    sa.Column("url", sa.String),
    sa.Column(
        "name",
        sa.String,
        sa.CheckConstraint(
            sa.text("name != ''"), name="ck_project_name_not_empty"
        ),
        unique=True,
        nullable=False,
    ),
    sa.Column("description", sa.String),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    sa.Column(
        "modified_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    sa.Column(
        "large_data_id",
        sa.dialects.postgresql.OID,
        nullable=True,
        comment="OID of large object containing project files.",
    ),
)

inventories = sa.Table(
    "inventory",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        sa.Identity(always=True),
        primary_key=True,
    ),
    sa.Column("name", sa.String),
    sa.Column("inventory", sa.String),
    sa.Column(
        "project_id",
        sa.ForeignKey("project.id", ondelete="CASCADE"),
        nullable=True,
    ),
)


extra_vars = sa.Table(
    "extra_var",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        sa.Identity(always=True),
        primary_key=True,
    ),
    sa.Column("name", sa.String),
    sa.Column("extra_var", sa.String),
    sa.Column(
        "project_id",
        sa.ForeignKey("project.id", ondelete="CASCADE"),
        nullable=True,
    ),
)

playbooks = sa.Table(
    "playbook",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        sa.Identity(always=True),
        primary_key=True,
    ),
    sa.Column("name", sa.String),
    sa.Column("playbook", sa.String),
    sa.Column(
        "project_id",
        sa.ForeignKey("project.id", ondelete="CASCADE"),
        nullable=True,
    ),
)
