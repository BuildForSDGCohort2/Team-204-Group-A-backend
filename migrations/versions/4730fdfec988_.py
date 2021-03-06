"""empty message

Revision ID: 4730fdfec988
Revises: eaf9e87ea82f
Create Date: 2020-09-30 21:50:47.932809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4730fdfec988'
down_revision = 'eaf9e87ea82f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointment_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.Column('details', sa.String(length=50), nullable=False),
    sa.Column('facility_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['facility_id'], ['facility.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointment_model')
    # ### end Alembic commands ###
