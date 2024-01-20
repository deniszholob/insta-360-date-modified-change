"""Changes the access and modified date of an insta360 file

When exporting insta360 video files or screen-grabs from a video files,
the files do not contain a date taken attribute.
Also the access/modified date is set to the exported date.

The default file name contains the full date/time info.

This script goes through all the jpg and mp4 files in a specified directory,
matching names similar to "VID_20221203_150437_00_028_20221204102048_clip1.mp4"
and updates the access and modified date from the extracted date/time from the file name.
"""

import os
import re
import time

# Get the list of files in the directory
directory = '/home/denis/Videos/insta360-exports'


def main():
    """Goes through all specified files in the directory"""
    files = os.listdir(directory)

    # Iterate over the files
    for file in files:
        if file.endswith(tuple(['.mp4', '.jpg'])):
            process_file(file)


def process_file(file):
    video_file = os.path.join(directory, file)
    date_time_match = match_video_file(file)

    print(f'"{video_file}" - Path')

    if date_time_match:
        # Get the date/time from the regular expression match
        date_str = date_time_match.group(1)
        time_str = date_time_match.group(2)
        change_date_time_for_file(video_file, date_str, time_str)

    else:
        print(f'"{video_file}" - Failed to parse the date/time for this file.')


def change_date_time_for_file(video_file, date_str, time_str):
    """Sets the date/time for the file modified date based on the inputs"""
    # Convert the date/time strings to a timestamp (in seconds since epoch)
    date_time_str = f'{date_str} {time_str}'
    date_time = time.strptime(date_time_str, '%Y%m%d %H%M%S')
    timestamp = time.mktime(date_time)

    # Get the current date modification value
    date_modified = os.path.getmtime(video_file)

    # Set the new date access and modified times
    os.utime(video_file, (timestamp, timestamp))

    # Confirm that the date modification value has been changed
    new_date_modified = os.path.getmtime(video_file)

    # Convert the timestamps to date/time strings for printing
    date_modified_str = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(date_modified))
    new_date_modified_str = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(new_date_modified))

    if date_modified != new_date_modified:
        print(f'"{video_file}" - The date taken value has been successfully changed from "{date_modified_str}" to "{new_date_modified_str}"')
    else:
        print(f'"{video_file}" - Failed to change the date created value. OLD: "{date_modified_str}", NEW: "{new_date_modified_str}"')


def match_video_file(file):
    """Tries to match the date/time file pattern in in the name"""
    # Set the path to the mp4 file
    # video_file = 'w:/2022/2022-12-03-Brighton Snowboard/360x3-exports/test/VID_20221203_150437_00_028-Denis-Roll.mp4'
    video_file = os.path.join(directory, file)
    # video_file = os.path.abspath(video_file_rel)

    # Parse the date/time from the file name using a regular expression
    date_time_pattern = r'VID_(\d{8})_(\d{6})'
    date_time_match = re.search(date_time_pattern, video_file)
    return date_time_match


# Using the special python variable __name__ to
if __name__ == "__main__":
    main()
#     print("Script is being run directly")
# else:
#     print("Script is being imported")
