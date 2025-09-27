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


#function to download a preview of the chosen artist's track
def download_preview(artists, save_path):

    artist_name = artists[0]
    # Step 1: Search artist
    search_url = f"https://api.deezer.com/search/artist?q={artist_name}"
    res = requests.get(search_url).json()
    if not res.get("data"):
        print("Artist not found.")
        return None
    
    artist_id = res["data"][0]["id"]

    # Step 2: Get artist's top tracks
    top_tracks_url = f"https://api.deezer.com/artist/{artist_id}/top?limit=1"
    res = requests.get(top_tracks_url).json()
    if not res.get("data"):
        print("No tracks found.")
        return None
    
    track = res["data"][0]
    preview_url = track["preview"]

    # Step 3: Download the preview
    r = requests.get(preview_url)
    if r.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"Downloaded: {track['title']} by {track['artist']['name']} → {save_path}")
        return save_path
    else:
        print("Failed to download preview.")
        return None

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

