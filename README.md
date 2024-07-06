```markdown
# iCloud Shared Album Downloader

This script allows you to download photos from a shared iCloud album. You can download all photos or a single random photo while keeping track of previously downloaded photos to avoid duplicates.

## Features

- Download all photos from a shared iCloud album.
- Download a single random photo and save it with a specified filename.
- Keep track of previously downloaded photos to avoid duplicates.

## Requirements

- Python 3.x
- `requests` library

You can install the `requests` library using pip:

```sh
pip install requests
```

## Usage

### Download All Photos

To download all photos from the album:

```sh
python iclouder.py <your_token>
```

### Download a Single Random Photo

To download a single random photo and save it as `random_photo.jpg`:

```sh
python iclouder.py <your_token> --single --filename random_photo.jpg
```

### Download All Photos to a Specific Directory

To download all photos to a specific directory:

```sh
python iclouder.py <your_token> --destination /path/to/directory
```

### Ignore Previously Downloaded Photos

To specify the number of previously downloaded photos to ignore:

```sh
python iclouder.py <your_token> --single --filename random_photo.jpg --ignore 50
```

### Enable Debug Logging

To enable debug logging for more detailed output:

```sh
python iclouder.py <your_token> --debug
```

### Note on Token

The token is the part of the URL after the `#` (and before any potential semicolon). The tokens seem to be 15 characters long.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
