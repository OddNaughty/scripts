import argparse
from MyMusic import MyMusic

def main(url, path):
    """
    Requirements: youtube_dl, mutagen
    """
    if not path:
        mytag = MyMusic()
    else:
        mytag = MyMusic(path)
    mytag.get_song_from_yt(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to download a youtube/soundcloud video and convert to mp3")
    parser.add_argument('url')
    parser.add_argument('-yt_path', help="The directory to store the converted files")
    args = parser.parse_args()
    main(args.url, args.yt_path)