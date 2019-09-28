"""super massive migration

Revision ID: 7397864c53bb
Revises: 
Create Date: 2019-09-28 10:19:28.901019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7397864c53bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('information_sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('organizers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('position', sa.String(), nullable=False),
    sa.Column('social_link', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('partners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('link', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('volunteer_logins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vk_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vk_id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('can_apply', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('importance', sa.Integer(), nullable=False),
    sa.Column('base_karma_to_pay', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('issue_date', sa.DateTime(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('issued_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['issued_by_id'], ['organizers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organizers_projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organizer_id'], ['organizers.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('volunteers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('volunteer_id', sa.String(), nullable=False),
    sa.Column('karma', sa.Integer(), server_default='0', nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.Column('work', sa.String(), nullable=False),
    sa.Column('speciality', sa.String(), nullable=True),
    sa.Column('food_preferences', sa.Enum('vegetarian', 'vegan', 'halal', 'kosher', 'nut_allergy', name='foodpreferences'), nullable=True),
    sa.Column('volunteering_experience', sa.Text(), nullable=True),
    sa.Column('interested_in_projects', sa.Text(), nullable=False),
    sa.Column('children_work_experience', sa.Text(), nullable=False),
    sa.Column('additional_skills', sa.String(), nullable=False),
    sa.Column('reasons_to_work', sa.String(), nullable=False),
    sa.Column('expectations', sa.Text(), nullable=True),
    sa.Column('medical_contradictions', sa.Text(), nullable=True),
    sa.Column('cloth_size', sa.Enum('XS', 'S', 'M', 'L', 'XL', 'XXL', name='clothsize'), nullable=False),
    sa.Column('accept_news', sa.Boolean(), server_default='t', nullable=True),
    sa.Column('login_id', sa.Integer(), nullable=True),
    sa.Column('known_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['known_by_id'], ['information_sources.id'], ),
    sa.ForeignKeyConstraint(['login_id'], ['volunteer_logins.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('volunteer_id')
    )
    op.create_table('event_schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time_begin', sa.Time(), nullable=False),
    sa.Column('time_end', sa.Time(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organizers_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['organizer_id'], ['organizers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('max_people', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('volunteer_language_associations',
    sa.Column('proficiency', sa.Integer(), nullable=False),
    sa.Column('volunteer_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['volunteers.id'], ),
    sa.PrimaryKeyConstraint('volunteer_id', 'language_id')
    )
    op.create_table('volunteer_tags',
    sa.Column('volunteer_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['volunteers.id'], )
    )
    op.create_table('events_volunteers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('volunteer_id', sa.Integer(), nullable=False),
    sa.Column('karma_to_pay', sa.Integer(), nullable=False),
    sa.Column('need_paper_certificate', sa.Boolean(), nullable=False),
    sa.Column('motivation', sa.String(), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('participation_status', sa.Enum('APPROVED', 'WAITING', 'KICKED', 'DECLINED', 'PLANNED', name='participationstatus'), nullable=False),
    sa.Column('actual_role_id', sa.Integer(), nullable=True),
    sa.Column('preferable_role1_id', sa.Integer(), nullable=True),
    sa.Column('preferable_role2_id', sa.Integer(), nullable=True),
    sa.Column('preferable_role3_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actual_role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['preferable_role1_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['preferable_role2_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['preferable_role3_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['volunteers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_done', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('organizer_event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organizer_event_id'], ['organizers_events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qr_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('salt', sa.String(), nullable=False),
    sa.Column('event_volunteer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_volunteer_id'], ['events_volunteers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('qr_data')
    op.drop_table('todos')
    op.drop_table('events_volunteers')
    op.drop_table('volunteer_tags')
    op.drop_table('volunteer_language_associations')
    op.drop_table('roles')
    op.drop_table('organizers_events')
    op.drop_table('event_schedule')
    op.drop_table('volunteers')
    op.drop_table('organizers_projects')
    op.drop_table('invites')
    op.drop_table('events')
    op.drop_table('volunteer_logins')
    op.drop_table('tags')
    op.drop_table('projects')
    op.drop_table('partners')
    op.drop_table('organizers')
    op.drop_table('languages')
    op.drop_table('information_sources')
    # ### end Alembic commands ###