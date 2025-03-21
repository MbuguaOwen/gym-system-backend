"""Initial migration

Revision ID: 1ad79fc3e24a
Revises: 
Create Date: 2025-03-21 17:25:38.697318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ad79fc3e24a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admins', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('admins', 'password_hash',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
    op.drop_constraint('admins_email_key', 'admins', type_='unique')
    op.create_index(op.f('ix_admins_email'), 'admins', ['email'], unique=True)
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    op.alter_column('members', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('members', 'phone_number',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.drop_constraint('members_email_key', 'members', type_='unique')
    op.create_index(op.f('ix_members_email'), 'members', ['email'], unique=True)
    op.create_index(op.f('ix_members_id'), 'members', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_members_id'), table_name='members')
    op.drop_index(op.f('ix_members_email'), table_name='members')
    op.create_unique_constraint('members_email_key', 'members', ['email'])
    op.alter_column('members', 'phone_number',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('members', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_index(op.f('ix_admins_id'), table_name='admins')
    op.drop_index(op.f('ix_admins_email'), table_name='admins')
    op.create_unique_constraint('admins_email_key', 'admins', ['email'])
    op.alter_column('admins', 'password_hash',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.alter_column('admins', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
