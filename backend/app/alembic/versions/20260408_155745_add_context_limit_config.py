"""Add context limit configuration to user_llm_configs

Revision ID: add_context_limit_config
Revises: 
Create Date: 2026-04-08 15:57:45

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_context_limit_config'
down_revision = None  # Update this with the previous revision if needed
branch_labels = None
depends_on = None


def upgrade():
    """Add context limit configuration columns"""
    # Add max_context_tokens column with default value
    op.add_column('user_llm_configs', 
        sa.Column('max_context_tokens', sa.Integer(), nullable=True, server_default='200000')
    )
    
    # Add other memory management columns
    op.add_column('user_llm_configs',
        sa.Column('max_conv_cache', sa.Float(), nullable=True, server_default='0.6')
    )
    
    op.add_column('user_llm_configs',
        sa.Column('summarize_word_limit', sa.Integer(), nullable=True, server_default='250')
    )
    
    op.add_column('user_llm_configs',
        sa.Column('cache_evict_prop', sa.Float(), nullable=True, server_default='0.5')
    )


def downgrade():
    """Remove context limit configuration columns"""
    op.drop_column('user_llm_configs', 'cache_evict_prop')
    op.drop_column('user_llm_configs', 'summarize_word_limit')
    op.drop_column('user_llm_configs', 'max_conv_cache')
    op.drop_column('user_llm_configs', 'max_context_tokens')
