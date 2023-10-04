import csv
import getopt, sys
from moviepy.video import fx
from moviepy.editor import VideoFileClip, concatenate_videoclips, cvsecs, CompositeVideoClip, TextClip, vfx

global folder
global event
global mp4_file
global config_file

folder = '/Videos/'
# file name of the video and config file
event = 'my_sample'

def return_filename(desc, prefix, suffix):
    return str(prefix or '') + str(desc or '') + str(suffix or '') + '.mp4'


def add_freeze_frame(clip, row):
    if 'add_freeze_sec' in row and int(row['add_freeze_sec']) > 0:
        result = fx.all.freeze(clip, t=0, freeze_duration=int(row['add_freeze_sec']))

        # Add description
        if 'add_desc_to_video' in row and row['add_desc_to_video'][:1].lower() == 'y' and row['desc']:
            txt_clip = TextClip(row['desc'], fontsize=50, color='white')
            # setting position of text in the center and duration will be 10 seconds 
            txt_clip = txt_clip.set_position(('left', 'bottom')).set_duration(int(row['add_freeze_sec']))
            # Overlay the text clip on the first video clip 
            result = CompositeVideoClip([result, txt_clip])

            # Add minute and seconds
        if 'add_time' in row and row['add_time'][:1].lower() == 'y':
            txt_clip = TextClip(str(row['min']) + ':' + str(row['sec']), fontsize=50, color='white')
            # setting position of text in the center and duration will be 10 seconds 
            txt_clip = txt_clip.set_position(('right', 'bottom')).set_duration(int(row['add_freeze_sec']))
            # Overlay the text clip on the first video clip 
            result = CompositeVideoClip([result, txt_clip])

        return result

    else:
        return clip


def main():
    global folder
    global event
    global mp4_file
    global config_file

    mp4_file = folder + '/' + event + '.mp4'
    config_file = folder + '/' + event + '.csv'
    argumentlist = sys.argv[1:]

    options = "i:c:"

    long_options = ["input=", "config=", "output="]

    output_file = None

    try:
        arguments, values = getopt.getopt(argumentlist, options, long_options)
        for current_argument, current_value in arguments:
            if current_argument in ("-i", "--input"):
                mp4_file = current_value
            if current_argument in ("-c", "--config"):
                config_file = current_value
    except getopt.error as err:
        print(str(err))

    if mp4_file is None:
        # If mp4 file is not provided, use config file name
        mp4_file = config_file.replace(".csv", ".mp4")

    # Read the config file
    rows = csv.DictReader(open(config_file))
    fields = rows.fieldnames

    # Get the distinct tags to s
    s = set(())
    for r in rows:
        s.add(r['filename_suffix'].lower())

    for keytext in s:
        first = True
        final_clip = None
        rows = csv.DictReader(open(config_file))
        for row in rows:
            if row['source'] == 'video' and row["filename_suffix"].lower() == keytext:
                min = int(row['min'])
                sec = int(row['sec'])

                if min > 0:
                    start_seconds = min * 60 + sec
                else:
                    start_seconds = sec
                length_in_sec = int(row['length_in_sec'])
                end_seconds = start_seconds + length_in_sec
                if start_seconds and end_seconds:
                    clip = VideoFileClip(mp4_file).subclip(start_seconds, end_seconds)
                    fclip = add_freeze_frame(clip, row)
                    if final_clip:
                        final_clip = concatenate_videoclips([final_clip, fclip])
                    else:
                        final_clip = fclip
                else:
                    print(f'Error with config settings for: {row}')

        final_clip.write_videofile(folder + "/" + event + ' ' + keytext + '.mp4', codec="libx264")


if __name__ == "__main__":
    main()
