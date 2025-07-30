"""make shop_id nullable

Revision ID: 7004b488ea6f
Revises: 0bae1014b5aa
Create Date: 2025-07-30 10:10:47.015700

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7004b488ea6f'
down_revision = '0bae1014b5aa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        'products',
        'shop_id',
        existing_type=sa.Integer(),
        nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        'products',
        'shop_id',
        existing_type=sa.Integer(),
        nullable=False
    )
