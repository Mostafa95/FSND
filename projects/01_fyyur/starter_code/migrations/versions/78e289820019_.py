"""empty message

Revision ID: 78e289820019
Revises: 
Create Date: 2019-12-21 23:58:40.333801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78e289820019'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('genres', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('genres', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


     ## Populate Artist ##
    op.execute("insert into \"Artist\"(name,city,state,phone,image_link,facebook_link,genres,website,seeking_venue,seeking_description)\
                values('Guns N Petals','SAN FRANCISCO','NY','326-123-5000','https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',\
                        'https://www.facebook.com/GunsNPetals',\'{\"Rock n Roll\"}\','https://www.gunsnpetalsband.com',True,'Looking for shows to perform at in the San Francisco Bay Area!');")

    op.execute("Insert into \"Artist\"(name,city,state,phone,image_link,facebook_link,genres,website,seeking_venue,seeking_description)\
                values('Matt Quevedo','NEW YORK','NY','300-400-5000','https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',\
                        'https://www.facebook.com/mattquevedo923251523',\'{\"Jazz\"}\','',False,'');")

    op.execute("Insert into \"Artist\"(name,city,state,phone,image_link,facebook_link,genres,website,seeking_venue,seeking_description)\
                values('The Wild Sax Band','SAN FRANCISCO','CA','432-325-5432','https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',\
                        '',\'{\"Jazz\",\"Classical\"}\','',False,'');")

    ## Populate Venue ##
    op.execute("insert into \"Venue\"(name,city,state,Address,phone,image_link,facebook_link,genres,website,seeking_talent,seeking_description)\
                values('The Musical Hop','SAN FRANCISCO','CA','1015 Folsom Street','123-123-1234','https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',\
                        'https://www.facebook.com/TheMusicalHop',\'{\"Jazz\",\"Reggae\",\"Swing\",\"Classical\",\"Folk\"}\','https://www.themusicalhop.com',True,'We are on the lookout for a local artist to play every two weeks. Please call us.');")

    op.execute("insert into \"Venue\"(name,city,state,Address,phone,image_link,facebook_link,genres,website,seeking_talent,seeking_description)\
                values('The Dueling Pianos Bar','NEW YORK','NY','335 Delancey Street','914-003-1132','https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',\
                        'https://www.facebook.com/theduelingpianos',\'{\"R&B\",\"Hip-Hop\",\"Classical\"}\','https://www.theduelingpianos.com',False,'');")

    op.execute("insert into \"Venue\"(name,city,state,Address,phone,image_link,facebook_link,genres,website,seeking_talent,seeking_description)\
                values('Park Square Live Music & Coffee','SAN FRANCISCO','CA','34 Whiskey Moore Ave','415-000-1234','https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',\
                        'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',\'{\"Rock n Roll\",\"Jazz\",\"Classical\",\"Folk\"}\','https://www.parksquarelivemusicandcoffee.com',False,'');")
    
    ## Populate Shows ##
    op.execute("insert into \"Shows\"(artist_id,venue_id,start_time)\
                values(1,1,'2019-05-21T21:30:00.000Z');")
    
    op.execute("insert into \"Shows\"(artist_id,venue_id,start_time)\
                values(2,3,'2019-06-15T23:00:00.000Z');")

    op.execute("insert into \"Shows\"(artist_id,venue_id,start_time)\
                values(3,3,'2035-04-01T20:00:00.000Z');")
    
    op.execute("insert into \"Shows\"(artist_id,venue_id,start_time)\
                values(3,3,'2035-04-08T20:00:00.000Z');")
    
    op.execute("insert into \"Shows\"(artist_id,venue_id,start_time)\
                values(3,3,'2035-04-15T20:00:00.000Z');")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Shows')
    op.drop_table('Venue')
    op.drop_table('Artist')
    # ### end Alembic commands ###
