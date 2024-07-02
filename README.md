# iCloud Shared Album Downloader

This script allows you to download photos from a public iCloud shared album. You can either download all photos or a single random photo. The downloaded photos can be saved to a specified directory.

## Requirements

- Python 3.x
- `requests` library

You can install the required library using pip:
```sh
pip install requests
```

## Usage

### Download All Photos
To download all photos from the album, use the following command:

```sh
python iclouder.py <your_token>
```

### Download a Single Random Photo
To download a single random photo and save it as `random_photo.jpg`, use the following command:

```sh
python iclouder.py <your_token> --single --filename random_photo.jpg
```

### Download All Photos to a Specific Directory
To download all photos to a specific directory, use the following command:

```sh
python iclouder.py <your_token> --destination /path/to/directory
```

### Debug Mode
You can enable debug mode to see more detailed logging information:

```sh
python iclouder.py <your_token> --debug
```

### Full Command-Line Options

```
usage: iclouder.py [-h] [--debug] [--destination DESTINATION] [--single] [--filename FILENAME] token

positional arguments:
  token                 The token part of the shared iCloud album

optional arguments:
  -h, --help            show this help message and exit
  --debug               Show logs up to debug level.
  --destination DESTINATION
                        Destination directory for downloads.
  --single              Download a single random photo.
  --filename FILENAME   Fixed filename for the downloaded photo (overwrites each time).
```

# Notes

- Ensure that the destination directory exists before running the script.
- The `token` is the unique identifier for your shared iCloud album.
- Note the token is the part of URL after the `#` (and before any potential semicolon). The tokens seem to be 15 characters long.
