"""initial schema

Revision ID: dd33cb03d01f
Revises:
Create Date: 2021-11-09 18:53:32.308761

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dd33cb03d01f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cc", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("price", sa.Float()),
        sa.Column("quantity", sa.Float()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("orders")
