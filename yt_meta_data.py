import argparse
from MyMusic import MyMusic

def main(url):
    """
    Requirements: youtube_dl, mutagen
    """
    mytag = MyMusic()
    mytag.get_song_from_yt(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to download a youtube/soundcloud video and convert to mp3")
    parser.add_argument('url')
    args = parser.parse_args()
    main(args.url)