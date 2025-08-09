import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('models/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def seed_db():
    """Seed the database with initial data."""
    db = get_db()
    with current_app.open_resource('models/seed_data.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('seed-db')
def seed_db_command():
    """Load seed data into the database."""
    seed_db()
    click.echo('Seeded the database with initial data.')

def seed_db_email():
    """Seed the database with initial data."""
    db = get_db()
    with current_app.open_resource('models/test_notification.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('email-db')
def seed_db_email_command():
    """Load testing email data into the database."""
    seed_db()
    click.echo('Seeded the database with data testing email notification system.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(seed_db_email_command)
