import deezer
import os
import requests

ARTIST_OPTIONS_A = ['Weeknd', 'Bruno', 'Rihanna', 'Billie', 'Taylor']
ARTIST_OPTIONS_B = ['Arianna', "Olivia", "Michael", "Malone", "Sabrina"]

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

def set_cover(player_x, type, save_dir="assets/album-covers"):
    main_artist = player_x[0]

    # Pick the right dictionary
    if main_artist in SONG_OPTIONS_A:
        cover_url = SONG_OPTIONS_A[main_artist][0]["album_cover"]
    else:
        cover_url = SONG_OPTIONS_B[main_artist][0]["album_cover"]

    # Save path (e.g. assets/covers/Weeknd.jpg)
    safe_name = f"player_{type}"
    save_path = os.path.join(save_dir, f"{safe_name}.jpg")

    # Download the image
    r = requests.get(cover_url)
    if r.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(r.content)
        return save_path
    else:
        raise ValueError(f"Could not download cover for {main_artist} from {cover_url}")
if __name__ == "__main__":
    # for artist, songs in SONG_OPTIONS_A.items():
    #     print(f"{artist}:")
    #     for s in songs:
    #         print(f" - {s['title']} ({s['album_cover']})")
    #     print()

    # for artist, songs in SONG_OPTIONS_B.items():
    #     print(f"{artist}:")
    #     for s in songs:
    #         print(f" - {s['title']} ({s['album_cover']})")
    #     print()

    player_a = ""
    set_cover(player_a, ["The Weeknd", "Taylor Swift"])

