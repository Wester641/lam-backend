"""fix(product): make fields other than title nullable

Revision ID: 19c4a10af4ce
Revises: 0ee3bdd330b7
Create Date: 2025-09-28 15:41:57.036127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19c4a10af4ce'
down_revision: Union[str, Sequence[str], None] = '0ee3bdd330b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - SQLite compatible version."""
    # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
    
    # Create new table with updated schema
    op.create_table('products_new',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=True),  # Changed to nullable
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('short_description', sa.Text(), nullable=True),
        sa.Column('sku', sa.String(length=50), nullable=True),  # Changed to nullable
        sa.Column('base_price', sa.Float(), nullable=True),  # Changed to nullable
        sa.Column('old_price', sa.Float(), nullable=True),
        sa.Column('stock_state', sa.String(length=20), nullable=True),
        sa.Column('total_stock', sa.Integer(), nullable=True),
        sa.Column('min_order_quantity', sa.Integer(), nullable=True),
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),  # Changed to nullable
        sa.Column('brand_id', sa.Integer(), nullable=True),
        sa.Column('shop_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
        sa.UniqueConstraint('sku'),
        sa.UniqueConstraint('slug')
    )
    
    # Copy data from old table to new table
    op.execute("""
        INSERT INTO products_new (
            id, title, slug, description, short_description, sku, base_price, 
            old_price, stock_state, total_stock, min_order_quantity, meta_title, 
            meta_description, category_id, brand_id, shop_id, is_active, 
            is_featured, created_at, updated_at
        )
        SELECT 
            id, title, slug, description, short_description, sku, base_price, 
            old_price, stock_state, total_stock, min_order_quantity, meta_title, 
            meta_description, category_id, brand_id, shop_id, is_active, 
            is_featured, created_at, updated_at
        FROM products
    """)
    
    # Drop old table
    op.drop_table('products')
    
    # Rename new table to original name
    op.rename_table('products_new', 'products')
    
    # Recreate indexes
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema - SQLite compatible version."""
    # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
    
    # Create new table with original schema (NOT NULL constraints)
    op.create_table('products_new',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),  # Back to NOT NULL
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('short_description', sa.Text(), nullable=True),
        sa.Column('sku', sa.String(length=50), nullable=False),  # Back to NOT NULL
        sa.Column('base_price', sa.Float(), nullable=False),  # Back to NOT NULL
        sa.Column('old_price', sa.Float(), nullable=True),
        sa.Column('stock_state', sa.String(length=20), nullable=True),
        sa.Column('total_stock', sa.Integer(), nullable=True),
        sa.Column('min_order_quantity', sa.Integer(), nullable=True),
        sa.Column('meta_title', sa.String(length=255), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),  # Back to NOT NULL
        sa.Column('brand_id', sa.Integer(), nullable=True),
        sa.Column('shop_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
        sa.UniqueConstraint('sku'),
        sa.UniqueConstraint('slug')
    )
    
    # Copy data from old table to new table (only rows with non-null required fields)
    op.execute("""
        INSERT INTO products_new (
            id, title, slug, description, short_description, sku, base_price, 
            old_price, stock_state, total_stock, min_order_quantity, meta_title, 
            meta_description, category_id, brand_id, shop_id, is_active, 
            is_featured, created_at, updated_at
        )
        SELECT 
            id, title, slug, description, short_description, sku, base_price, 
            old_price, stock_state, total_stock, min_order_quantity, meta_title, 
            meta_description, category_id, brand_id, shop_id, is_active, 
            is_featured, created_at, updated_at
        FROM products
        WHERE slug IS NOT NULL 
          AND sku IS NOT NULL 
          AND base_price IS NOT NULL 
          AND category_id IS NOT NULL
    """)
    
    # Drop old table
    op.drop_table('products')
    
    # Rename new table to original name
    op.rename_table('products_new', 'products')
    
    # Recreate indexes
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
