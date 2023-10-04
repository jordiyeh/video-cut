# video-cut
Cut a full length video event into individual files or combined highlights using a CSV file

Edit .venv/lib/python3.10/site-packages/moviepy/config_defaults.py and update IMAGEMAGICK_BINARY variable with proper path, such as

IMAGEMAGICK_BINARY = "/opt/homebrew/bin/convert"

or add environmental variable IMAGEMAGICK_BINARY

#IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'auto-detect')
