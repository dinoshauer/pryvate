"""Pryvate database: SQLite."""
import sqlite3


class PryvateSQLite(object):

    """Use SQLite to save egg information.

    Attempts to create the ``eggs`` table if
    it does not already exist.

    Keyword Arguments:
        name (``str``, optional): Path to the database
            *Default:* ``pryvate.db``
    """

    CREATE_EGG_TABLE = '''CREATE TABLE IF NOT EXISTS eggs
    (
        name TEXT, description TEXT, license TEXT,
        author TEXT, author_email TEXT, download_url TEXT,
        summary TEXT, platform TEXT, metadata_version TEXT,
        home_page TEXT
    );'''
    CREATE_VERSION_TABLE = '''CREATE TABLE IF NOT EXISTS versions
    (
        name TEXT, version TEXT,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );'''
    GET_ALL_PIP = 'SELECT name FROM eggs;'
    GET_ALL_API = '''SELECT eggs.*, versions.version, versions.upload_date
    FROM eggs
    INNER JOIN versions ON eggs.name = versions.name
    /*Get only the latest version here*/
    LIMIT :limit OFFSET :offset;'''
    NEW_EGG = '''INSERT INTO eggs (
        name, description, license, author, author_email, download_url,
        summary, platform, metadata_version, home_page
    ) VALUES (
        :name, :description, :license, :author, :author_email, :download_url,
        :summary, :platform, :metadata_version, :home_page
    );'''
    NEW_VERSION = '''INSERT INTO versions (
        name, version
    ) VALUES (
        :name, :version
    );'''

    def __init__(self, name='pryvate.db'):
        """Initialize a new database connection."""
        self.connection = sqlite3.connect(name)
        self.connection.execute(self.CREATE_EGG_TABLE)
        self.connection.execute(self.CREATE_VERSION_TABLE)
        self.connection.commit()
        self.connection.row_factory = sqlite3.Row

    def get_eggs_pip(self):
        """Get available private eggs (PIP).

        Returns:
            ``list`` of ``str``
        """
        rows = self.connection.execute(self.GET_ALL_PIP)
        return [item['name'] for item in rows]

    def get_eggs_api(self, limit, offset):
        """Get available private eggs (API).

        Returns:
            ``list`` of ``dict``
        """
        rows = self.connection.execute(self.GET_ALL_API,
                                       {'limit': limit, 'offset': offset})
        return [dict(row) for row in rows]

    def new_egg(self, data):
        """Add new egg to list.

        Arguments:
            data (``dict``): The data of the egg to add

        Returns:
            ``bool``
        """
        egg_insert = self.connection.execute(self.NEW_EGG, data)
        version_insert = self.connection.execute(self.NEW_VERSION, data)
        self.connection.commit()
        return bool(egg_insert.rowcount) and bool(version_insert.rowcount)
