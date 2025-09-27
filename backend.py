import deezer
import requests

ARTIST_OPTIONS_A = ['Weeknd', 'Bruno Mars', 'Rihanna', 'Billie Eilish', 'Taylor Swift']
ARTIST_OPTIONS_B = ['Arianna Grande', "Olivia Rodrigo", "Michael Jackson", "Malone", "Sabrina Carpenter"]

def get_top_10_with_covers(artist_name):
    """
    Returns top 10 tracks for the artist along with album cover URLs.
    """
    client = deezer.Client()
    
    # Search artist by name
    search_results = client.search_artists(artist_name)
    if not search_results:
        return []
    
    artist_obj = search_results[0]  # first matching artist

    # artist_obj.tracklist is a URL to the top tracks
    response = requests.get(f"{artist_obj.tracklist}?limit=10")
    if response.status_code != 200:
        return []
    
    data = response.json().get('data', [])
    
    tracks_with_covers = []
    for track in data:
        tracks_with_covers.append({
            'title': track['title'],
            'album_cover': track['album']['cover_medium']  # medium size cover
        })
    
    return tracks_with_covers

# Build SONG_OPTIONS dict
SONG_OPTIONS_A = {artist: get_top_10_with_covers(artist)[:5] for artist in ARTIST_OPTIONS_A}
SONG_OPTIONS_B = {artist: get_top_10_with_covers(artist)[:5] for artist in ARTIST_OPTIONS_B}

if __name__ == "__main__":
    for artist, songs in SONG_OPTIONS_A.items():
        print(f"{artist}:")
        for s in songs:
            print(f" - {s['title']} ({s['album_cover']})")
        print()

    for artist, songs in SONG_OPTIONS_B.items():
        print(f"{artist}:")
        for s in songs:
            print(f" - {s['title']} ({s['album_cover']})")
        print()
