# tja2sono

Convert TJA to Sonolus Taiko level

## Setup

Add repository folder to PATH in order to access script in other directories.

If you want to extract bgm, you also need [ffmepg](https://ffmpeg.org/) installed and in your PATH.

## Usage

Find and download Taiko map you want to convert (this will be a folder with `.tja` and `.ogg` files).

Generate folder with level using:
```
tja2sono.py -x <FOLDER APTH>
```

After geneeration, you can change out `cover.png` and update `info.json` in the outputted level folder.

Final level folder can be moved to your Sonolus server's `source/levels` and packed with `sonolus-pack`.