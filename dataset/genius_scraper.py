from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from urllib.request import urlopen, Request
import requests
from pprint import pprint
import os
from tqdm import tqdm

BASE_URL = "https://genius.com/artists/"
GENIUS_API_KEY = "wiIge7GYszD0izELN20hNP7-xgvWZCdOHpv2TKCLBDpEgud0UMgg2Tm2YjPJP0qA"


def get_artist_info(artist_name, page):
    base_url = "https://api.genius.com"
    headers = {"Authorization": "Bearer " + GENIUS_API_KEY}
    search_url = base_url + "/search?per_page=10&page=" + str(page)
    data = {"q": artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


def get_songs_url(artist: str, max_songs: int = 100):
    current_page = 1
    songs_url = []
    finished = False

    while not finished:
        response = get_artist_info(artist, current_page)
        json = response.json()

        for song in json["response"]["hits"]:
            url = song["result"]["url"]
            if len(songs_url) < max_songs:
                songs_url.append(url)

        if len(songs_url) >= max_songs:
            finished = True
        current_page += 1

    return songs_url


def get_lyrics(url: str):
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    song_lyrics = []
    for lyrics in html.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL"):
        for elem in lyrics:
            song_sentences = elem.get_text(separator="<br>", strip=True).split("<br>")
            for sentence in song_sentences:
                if sentence != "":
                    song_lyrics.append(sentence)

    return song_lyrics


def main():
    ## GENRES = HIP_HOP/RAP/TRAP, ROCK, POP, INDIE, METAL

    rap_artists = [
        "Kendrick Lamar",
        "Cardi B",
        "Drake",
        "Nicki Minaj",
        "J. Cole",
        "Travis Scott",
        "Lil Wayne",
        "Megan Thee Stallion",
        "Future",
        "Eminem",
        "Jay-Z",
        "Kanye West",
        "Lil Uzi Vert",
        "A$AP Rocky",
        "Tyler, the Creator",
        "21 Savage",
        "Nas",
        "Logic",
        "Young Thug",
        "Big Sean",
    ]

    rock_artists = [
        "Led Zeppelin",
        "The Beatles",
        "Queen",
        "Pink Floyd",
        "The Rolling Stones",
        "Nirvana",
        "U2",
        "AC/DC",
        "The Who",
        "Metallica",
        "Guns N' Roses",
        "Radiohead",
        "Foo Fighters",
        "Coldplay",
        "Red Hot Chili Peppers",
        "Pearl Jam",
        "Linkin Park",
        "The Eagles",
        "Green Day",
        "The Killers",
    ]

    pop_artists = [
        "Taylor Swift",
        "Beyoncé",
        "Justin Bieber",
        "Ariana Grande",
        "Ed Sheeran",
        "Lady Gaga",
        "Shawn Mendes",
        "Katy Perry",
        "Bruno Mars",
        "Rihanna",
        "Dua Lipa",
        "Harry Styles",
        "Selena Gomez",
        "The Weeknd",
        "Billie Eilish",
        "Adele",
        "Sia",
        "Zayn Malik",
        "Madonna",
        "Maroon 5",
    ]

    indie_artists = [
        "Arctic Monkeys",
        "Vampire Weekend",
        "Tame Impala",
        "Florence + the Machine",
        "Alt-J",
        "Bon Iver",
        "The Strokes",
        "Foster the People",
        "Mumford & Sons",
        "Two Door Cinema Club",
        "The National",
        "Arcade Fire",
        "Of Monsters and Men",
        "Phoenix",
        "Hozier",
        "CHVRCHES",
        "Bastille",
        "Sufjan Stevens",
        "M83",
        "The Lumineers",
    ]

    metal_artists = [
        "Metallica",
        "Slayer",
        "Iron Maiden",
        "Black Sabbath",
        "Megadeth",
        "Pantera",
        "Tool",
        "Judas Priest",
        "Slipknot",
        "Opeth",
        "Mastodon",
        "Avenged Sevenfold",
        "System of a Down",
        "Gojira",
        "Nightwish",
        "Disturbed",
        "Meshuggah",
        "Lamb of God",
        "Ghost",
        "Trivium",
    ]

    genre = "metal"
    pbar = tqdm(metal_artists)
    for artist in pbar:
        pbar.set_description(f"Processing {artist}")
        urls = get_songs_url(artist, 100)
        for i, url in enumerate(urls):
            pbar.set_description(f"Processing {artist} - Song {i+1}")
            lyrics = get_lyrics(url)
            artist = artist.replace("/", "_")

            if not os.path.exists(f"./genius_dataset/{genre}"):
                os.makedirs(f"./genius_dataset/{genre}")
            if not os.path.exists(f"./genius_dataset/{genre}/{artist}"):
                os.makedirs(f"./genius_dataset/{genre}/{artist}")

            with open(
                f"./genius_dataset/{genre}/{artist}/{artist}_{i+1}.txt", "a"
            ) as file:
                for line in lyrics:
                    file.write(line + "\n")


if __name__ == "__main__":
    main()
