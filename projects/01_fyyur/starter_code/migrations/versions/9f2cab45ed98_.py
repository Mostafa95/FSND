"""empty message

Revision ID: 9f2cab45ed98
Revises: 78e289820019
Create Date: 2019-12-23 20:42:40.259721

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9f2cab45ed98'
down_revision = '78e289820019'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id',sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Shows')
    # ### end Alembic commands ###
    op.execute("insert into \"Show\"(artist_id,venue_id,start_time)\
                values(1,1,'2019-05-21T21:30:00.000Z');")
    
    op.execute("insert into \"Show\"(artist_id,venue_id,start_time)\
                values(2,3,'2019-06-15T23:00:00.000Z');")

    op.execute("insert into \"Show\"(artist_id,venue_id,start_time)\
                values(3,3,'2035-04-01T20:00:00.000Z');")
    
    op.execute("insert into \"Show\"(artist_id,venue_id,start_time)\
                values(3,3,'2035-04-08T20:00:00.000Z');")
    
    op.execute("insert into \"Show\"(artist_id,venue_id,start_time)\
                values(3,3,'2035-04-15T20:00:00.000Z');")

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Shows_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], name='Shows_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='Shows_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Shows_pkey')
    )
    op.drop_table('Show')
    # ### end Alembic commands ###
