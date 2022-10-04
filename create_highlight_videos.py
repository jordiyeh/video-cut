import csv
import getopt, sys
from moviepy.editor import VideoFileClip, concatenate_videoclips

folder = '/Videos/'
# file name of the video and config file
event = '20221002 PREECNLBVA'

output_file = None # Create a file for each segment
#output_file = 'check' # Compile the clips with a check flag
output_file = 'highlight' # Compile the clips with a highligh flag
#output_file = '20221002 EYF Segments.mp4' # compile all segments in the config file


# --input
mp4_file = folder + '/' + event + '.mp4'
    # --config
config_file = folder + '/' + event + '.csv'
# --output


def return_filename(desc, prefix, suffix):
    return str(prefix or '') + str(desc or '') + str(suffix or '') + '.mp4'

def main():
    global folder
    global event
    global output_file
    global mp4_file
    global config_file

    argumentList = sys.argv[1:]

    options = "i:c:o:"

    long_options = ["input=","config=","output="]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-i", "--input"):
                mp4_file = currentValue
                # print ("File: ", currentValue)
            if currentArgument in ("-o", "--output"):
                output_file = currentValue
            if currentArgument in ("-c", "--config"):
                config_file = currentValue
                # print ("Config: ", currentValue)
    except getopt.error as err:
        print (str(err))

    if mp4_file is None:
        # If mp4 file is not provided, use config file name
        mp4_file = config_file.replace(".csv", ".mp4")

    # Read the config file
    rows = csv.DictReader(open(config_file))

    first = True
    for row in rows:
        if row['source'] == 'video':
            min = int(row['min'])
            sec = int(row['sec'])
            
            if min > 0:
                start_seconds = min * 60 + sec
            else:
                start_seconds = sec
            length_in_sec = int(row['length_in_sec'])
            end_seconds = start_seconds + length_in_sec
            if start_seconds and end_seconds:
                if output_file is None:
                    # MODE = Split the segments into separate files
                    clip = VideoFileClip(mp4_file).subclip(start_seconds, end_seconds)
                    file_name = return_filename(row['desc'], row['filename_prefix'], row['filename_suffix'])
                    clip.write_videofile(file_name)
                else:
                    # MODE = Concatenate the segments into a single file
                    if (output_file == 'check' and row['filename_suffix'] == 'check') or \
                        (output_file == 'highlight' and row['filename_suffix'] == 'highlight') or \
                            (output_file != 'check' and output_file != 'highlight'):
                        # Save only if check or highlight or if all clips
                        if first:
                            final_clip = VideoFileClip(mp4_file).subclip(start_seconds, end_seconds)
                            first = False
                        else:
                            clip = VideoFileClip(mp4_file).subclip(start_seconds, end_seconds)
                            final_clip = concatenate_videoclips([final_clip,clip])
            else:
                print(f'Error with config settings for: {row}')

    if output_file:
        # Save the final clip
        if output_file == 'check':
            output_file = event + ' check.mp4'
        elif output_file == 'highlight':
            output_file = event + ' highlight.mp4'
        final_clip.write_videofile(output_file)
    

if __name__ == "__main__":
    main()