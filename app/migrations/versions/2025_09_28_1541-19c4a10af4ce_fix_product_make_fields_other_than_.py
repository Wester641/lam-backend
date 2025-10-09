"""fix(product): make fields other than title nullable

Revision ID: 19c4a10af4ce
Revises: 0ee3bdd330b7
Create Date: 2025-09-28 15:41:57.036127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '19c4a10af4ce'
down_revision: Union[str, Sequence[str], None] = '0ee3bdd330b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - PostgreSQL compatible version."""
    # For PostgreSQL we can use ALTER COLUMN directly
    op.alter_column('products', 'slug',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('products', 'sku',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('products', 'base_price',
               existing_type=sa.DOUBLE_PRECISION(),
               nullable=True)
    op.alter_column('products', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema - PostgreSQL compatible version."""
    # First, ensure we don't have NULL values in required fields
    op.execute("UPDATE products SET slug = 'temp-slug-' || id WHERE slug IS NULL")
    op.execute("UPDATE products SET sku = 'temp-sku-' || id WHERE sku IS NULL")
    op.execute("UPDATE products SET base_price = 0 WHERE base_price IS NULL")
    op.execute("UPDATE products SET category_id = (SELECT MIN(id) FROM categories) WHERE category_id IS NULL")
    
    # Then restore NOT NULL constraints
    op.alter_column('products', 'slug',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('products', 'sku',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('products', 'base_price',
               existing_type=sa.DOUBLE_PRECISION(),
               nullable=False)
    op.alter_column('products', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
