# PlexPlaylistImporter
Import M3U playlist into plex

Made this because all the other methods to import playlist have not worked for me. This method works by directly comparing paths of files in the plex library to paths in a m3u playlist. Will only work if the paths are the same. In the future I can add a Song Artist and Title based compare.

Make sure to put your Plex url and plex token in the plex_connection function.

Uses https://github.com/pkkid/python-plexapi

Used some code from https://github.com/PyCoding-A/plex.audio_folder_to_playlist it's what inspired me to make this.
