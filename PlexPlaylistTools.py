import os
from plexapi.server import PlexServer


'''
Opens plex connection. It needs to be feed the IP of the server and a plex token
https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
'''
def plex_connection():
    plex_base_url = "IP HERE"
    plex_token = "TOKEN HERE"
    # https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
    plex = PlexServer(plex_base_url, plex_token)
    print("Connected to: " + str(plex.myPlexAccount()).replace('<MyPlexAccount:https://plex.tv/user:', '').replace('>', ''))
    return plex


'''
compares m3u and plex paths against eachother if they match then the mus object added to a on going list mus_list.
after all the songs in the plex library are ran through then the playlist name and mus_list are passed to the playlist
creation api.
'''
def compare_m3u_plex_paths(plex, m3u_paths, playlist_name):
    # plex.library.refresh()
    # print(m3u_paths)
    mus_list = []
    for section in plex.library.sections():
        music = plex.library.section(section.title)
        if section.type == "artist":
            count = 0
            for mus in music.searchTracks():
                plexPath = mus.locations[0]
                # print("\nTitle: {}\n Path: {}".format(mus.title, plexPath))  # Print every song in library
                if plexPath in m3u_paths:
                    print("\nAdded: \n Title: {}\n Path: {}".format(mus.title, plexPath))
                    mus_list.append(mus)
                    count = count + 1
            print("Found {} Track(s) out of {} Track(s)".format(count, len(m3u_paths)))  # Print every song added
            build_playlist(plex, mus_list, playlist_name)


'''
playlist creation takes the list of all of the music objects and creates a playlist with that list.
'''
def build_playlist(plex, mus_list, playlist_name):
    if mus_list:
        # checks if the playlist is made
        playlist = [playlist for playlist in plex.playlists() if playlist.title == playlist_name]
        for mus in mus_list:
            if not playlist:  # if playlist is not made then it creates it
                plex.createPlaylist(playlist_name, items=mus)
                playlist = [playlist for playlist in plex.playlists() if playlist.title == playlist_name]
            else:  # if playlist is made it adds one song to the playlist
                plex.playlist(playlist_name).addItems(mus)


'''
simple python text filtering to get the playlist paths from the m3u file.
This can be improved most likely. All it does is strip new line text, and add it to the paths list if it has a
forward slash. Won't work with all playlist files or OS's currently
'''
def load_m3u_playlist(M3UPath):
    M3U_Paths = []
    # M3UPath = input("Enter Path to m3u playlist:\n")
    with open(M3UPath, 'r', encoding='utf-8') as M3UFile:
        RawM3ULines = M3UFile.readlines()
    for line in RawM3ULines:
        line = line.replace("\n", "")
        if line[0] == '/':
            M3U_Paths.append(line)
    return M3U_Paths, os.path.basename(M3UPath)


'''
gets every file in folder and adds their paths to a list
'''
def load_all_playlists_in_folder(plex):
    playlist_dir = input("Enter Playlist Folder:\n")
    file_list = os.listdir(playlist_dir)
    path_list = []
    for file in file_list:
        path_list.append(playlist_dir + "\\" + file)
    return path_list


'''
little function to make main loop look better. takes the path of a m3u playlist and triggers the loading into plex.
'''
def load_m3u_path_into_plex(plex, m3uPath):
    m3u_paths, playlist_name = load_m3u_playlist(m3uPath)
    compare_m3u_plex_paths(Plex, m3u_paths, playlist_name)


'''
Main function, asks if it is loading a single file or folder and calls the trigger function
for loading a m3u path into plex.
'''
if __name__ == "__main__":
    Plex = plex_connection()
    if input("1: Folder\n2: Single File\n Please Enter 1 or 2:\n") == '1':
        for item in load_all_playlists_in_folder(Plex):
            load_m3u_path_into_plex(Plex, item)
    else:
        M3UPath = input("Enter Path to m3u playlist:\n")
        load_m3u_path_into_plex(Plex, M3UPath)
