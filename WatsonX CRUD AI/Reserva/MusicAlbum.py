# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2

class MusicAlbum:
    """Class representing a music album"""

    def __init__(self, title, artist, releaseYear, style):
        """Initialize a new music album

        Args:
            title (str): Title of the music album
            artist (str): Artist of the music album
            releaseYear (int):Year when the music album was released
            style (str): Style of the music album
        """
        self.title = title
        self.artist = artist
        self.releaseDate = releaseYear
        self.style = style

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
    def releaseYear(self):
        """Get the release year of the music album

        Returns:
            int: Release year of the music album
        """
        return self._releaseDate

    @releaseYear.setter
    def releaseYear(self, value):
        """Set the release year of the music album

        Args:
            value (int): New release year of the music album

        Raises:
            ValueError: If value is not a integer
        """
        assert isinstance(value, str), "release year must be an integer"
        self.__zip = value

    @property
    def style(self):
        """Get the style of the music album

        Returns:
            str: Style of the music album
        """
        return self._style

    @style.setter
    def style(self, value):
        """Set the style of the music album

        Args:
            value (str): New style of the music album

        Raises:
            ValueError: If value is not a string
        """
        assert isinstance(value, str), "Style must be a string"
        self._style = value