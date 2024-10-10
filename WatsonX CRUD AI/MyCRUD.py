# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import sqlite3

class MusicAlbum:
    """Class representing a music album"""

    def __init__(self, title, artist, year, genre):
        """Initialize a new music album

        Args:
            title (str): Title of the music album
            artist (str): Artist of the music album
            year (int):Year when the music album was released
            genre  (str): Genre of the music album
        """
        self.title = title
        self.artist = artist
        self.year = year
        self.genre  = genre

    @property
    def title(self):
        """Get the title of the music album

        Returns:
            str: Title of the music album
        """
        return self._title

    @title.setter
    def title(self, value):
        """Set the title of the music album

        Args:
            value (str): New title of the music album

        Raises:
            ValueError: If value is not a string
        """
        assert isinstance(value, str), "Title must be a string"
        self._title = value

    @property
    def artist(self):
        """Get the artist of the music album

        Returns:
            str: Artist of the music album
        """
        return self._artist

    @artist.setter
    def artist(self, value):
        """Set the artist of the music album

        Args:
            value (str): New artist of the music album

        Raises:
            ValueError: If value is not a string
        """
        assert isinstance(value, str), "Artist must be a string"
        self._artist = value

    @property
    def year(self):
        """Get the release year of the music album

        Returns:
            int: Release year of the music album
        """
        return self._year

    @year.setter
    def year(self, value):
        """Set the release year of the music album

        Args:
            value (int): New release year of the music album

        Raises:
            ValueError: If value is not a integer
        """
        assert isinstance(value, str), "release year must be an integer"
        self._year = value

    @property
    def genre(self):
        """Get the genre of the music album

        Returns:
            str: genre of the music album
        """
        return self._genre

    @genre.setter
    def genre(self, value):
        """Set the genre of the music album

        Args:
            value (str): New genre of the music album

        Raises:
            ValueError: If value is not a string
        """
        assert isinstance(value, str), "Genre must be a string"
        self._genre = value
        
class DatabaseConnection:
    """Class for interacting with a SQLite database."""

    def __init__(self, db_file):
        """Initialize the DatabaseConnection object.

        Args:
            db_file (str): The path to the SQLite database file.

        Raises:
            ValueError: If db_file is not a string.
        """

        if not isinstance(db_file, str):
            raise ValueError("db_file must be a string")
        
        self.conn = None
        self.db_file = db_file

    def connect(self):
        """Set the connection and cursor attributes."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("Connection established")
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def close(self):
        """Close the connection to the database."""
        if self.conn:
            self.conn.close()
            print("Connection closed")

    def create_table(self):
        """Create a table in the database if it doesn't already exist."""
        if self.conn:
            cursor = self.conn.cursor()
            sql = """CREATE TABLE IF NOT EXISTS music_albums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                year INTEGER NOT NULL,
                genre TEXT NOT NULL
            )"""
            cursor.execute(sql)
            self.conn.commit()
            print("Table created successfully")

    def add_album(self, title, artist, year, genre):
        """Add an album to the database.

        Args:
            title (str): The title of the album.
            artist (str): The artist of the album.
            year (int): The release year of the album.
            genre (str): The genre of the album.

        Raises:
            ValueError: If any of the arguments are not of the correct type.
        """
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if not isinstance(artist, str):
            raise ValueError("Artist must be a string")
        if not isinstance(year, int):
            raise ValueError("Year must be an integer")
        if not isinstance(genre, str):
            raise ValueError("Genre must be a string")

        sql = "INSERT INTO music_albums (title, artist, year, genre) VALUES (?, ?, ?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(sql, (title, artist, year, genre))
        self.conn.commit()
        print("The album was inserted")

    def get_all_albums(self):
        """Return a list of all albums in the database.

        Returns:
            list: A list of tuples representing each album in the database.
        """
        sql = "SELECT * FROM music_albums"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def delete_album(self, title):
        """Delete an album from the database.

        Args:
            title (str): The title of the album to delete.

        Raises:
            ValueError: If title is not a string.
        """
        if not isinstance(title, str):
            raise ValueError("Title must be a string")

        sql = "DELETE FROM music_albums WHERE title=?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (title,))
        self.conn.commit()
        print("The album was deleted")

    def update_album_year(self, old_year, new_year):
        """Update the release year of an album in the database.

        Args:
            old_year (int): The current release year of the album.
            new_year (int): The new release year of the album.

        Raises:
            ValueError: If either argument is not an integer.
        """
        if not isinstance(old_year, int):
            raise ValueError("Old year must be an integer")
        if not isinstance(new_year, int):
            raise ValueError("New year must be an integer")

        sql = "UPDATE music_albums SET year=? WHERE year=?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (new_year, old_year))
        self.conn.commit()
        print("The album was updated")

if __name__ == "__main__":
    db = DatabaseConnection("my_database.db")
    db.connect()
    # Use the database connection
    db.create_table()
    db.add_album("The Wall", "Pink Floyd", 1979, "Progressive")
    db.add_album("Ride the Lightning", "Metallica", 1984, "Heavy Metal")
    db.add_album("Aqualung", "Jethro Tull", 1971, "Progressive")
    list_of_albuns = db.get_all_albums()
    print(list_of_albuns)
    db.delete_album("The Wall")
    db.update_album_year(1979, 1980)
    db.close()