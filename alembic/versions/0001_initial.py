"""initial

Revision ID: 0001
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("external_id", sa.String, unique=True, nullable=False),
        sa.Column("source", sa.String, index=True),
        sa.Column("role", sa.String, index=True),
        sa.Column("experience_years", sa.Integer, default=0),
        sa.Column("skills_score", sa.Float, default=0.0),
        sa.Column("stage", sa.String, index=True),
        sa.Column("applied_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("offered", sa.Integer, default=0),
        sa.Column("hired", sa.Integer, default=0),
    )
    op.create_index("ix_candidates_stage_role", "candidates", ["stage", "role"])

def downgrade():
    op.drop_index("ix_candidates_stage_role", "candidates")
    op.drop_table("candidates")
