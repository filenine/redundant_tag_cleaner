# A script to clean up redundant "album artist" and "total discs" tags in my music collection
# Written starting 23 October 2023

"""
This program iterates through the audio files in a folder.

The code assumes that the given list of files are a single disc of an album.

If the "artist" tag is the same for all of the files and the value of the
"albumartist" tag is equal to the value of the "artist" tag, it deletes the
"albumartist" tag for all audio files in the folder.

Similarly, if the "disctotal" or "totaldiscs" tags have the value 1, the album
only has one disc, and the program deletes both the "total" tag and the
"discnumber" tag.
"""

import mutagen
import sys

def clean_redundant(files):
    """
    Cleans redundant tags
    
    Input: "files" - a list of files to be iterated over and cleaned up
    """
    print("Cleaning album artist tags...")
    clean_albumartist(files)
    print("Album artist tags cleaned!")
    print("Cleaning disc total tags...")
    clean_disctotal(files)
    print("Disc total tags cleaned!")

    print("Operations complete.")

def clean_albumartist(files):
    """
    Removes the "albumartist" tag if all tracks have the same artist and the
    value of the "albumartist" tag is equal to the value of the "artist" tags

    Input: "files" - a list of files to be iterated over and cleaned up
    """
    first_artist = mutagen.File(files[0])["artist"]
    album_has_single_artist = True # True by default, to handle single-track albums

    # "If the artist tag is the same for all of them"
    for file in files:
        if mutagen.File(file)["artist"] != first_artist:
            album_has_single_artist = False
            break # We already know the album has multiple artists - no need to keep looping
    
    # Check if the value of the albumartist tag is the same as the artist
    # If they're the same, delete the albumartist tag
    # This assumes every track has the same albumartist value
    if album_has_single_artist:
        if "albumartist" in mutagen.File(files[0]):
            if mutagen.File(files[0])["albumartist"] == first_artist:
                for file in files:
                    metadata = mutagen.File(file)
                    metadata.pop("albumartist", None)
                    metadata.save()

def clean_disctotal(files):
    """
    Removes the "discnumber", "disctotal" and "totaldiscs" tags if either
    the "disctotal" or "totaldiscs" tags are equal to 1

    Input: "files" - a list of files to be iterated over and cleaned up
    """
    for file in files:
        single_disc = False
        metadata = mutagen.File(file)
        if "disctotal" in metadata:
            if metadata["disctotal"][0] == u"1":
                single_disc = True
                metadata.pop("disctotal")
        if "totaldiscs" in metadata:
            if metadata["totaldiscs"][0] == u"1":
                single_disc = True
                metadata.pop("totaldiscs")
        if single_disc == True:
            if "discnumber" in metadata:
                metadata.pop("discnumber")

def main():
    files = sys.argv[1:]
    if files == []:
        print("No input files!")
    else:
        clean_redundant(files)

if __name__ == "__main__":
    main()
