import os
import tempfile
import json
import shutil
import subprocess
import argparse
from typing import Optional
from parsing import Parser
from conversion import convert_to_sonolus_info, convert_to_sonolus_data


def convert_level(
    input_dir: str,
    output_dir: str = "out/",
    cover_path: Optional[str] = None,
    extract_bgm: bool = False,
    verbose: bool = False
):
    # Find files
    tja_path = None
    ogg_path = None
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".tja"):
            tja_path = os.path.join(input_dir, file_name)
        elif file_name.endswith(".ogg"):
            ogg_path = os.path.join(input_dir, file_name)

    if verbose:
        if tja_path != None:
            print(f"Found TJA file: {tja_path}")
        if ogg_path != None:
            print(f"Found OGG file: {ogg_path}")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert OGG
        bgm_dir = os.path.join(temp_dir, "bgm.mp3")
        if extract_bgm and ogg_path != None:
            cmds = [
                "ffmpeg", "-i", ogg_path, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", bgm_dir
            ]
            if verbose:
                print(f"Converting to MP3...")
            code = subprocess.run(cmds).returncode
            if verbose:
                if code == 0:
                    print(f"Successfully converted!")
                else:
                    print(f"Error converting.")

        # Set cover path
        if cover_path == None:
            cover_path = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "assets/cover.png"
            )

        with open(tja_path, "r") as f:
            p = Parser(f)
            if verbose:
                print(f"Parsing {tja_path}...")
            p.parse()

            # Create levels
            for course in p.courses:
                level_dir = os.path.join(output_dir, course.slug)
                os.makedirs(level_dir, exist_ok=True)

                # Info
                if verbose:
                    print(f"[{course.slug}] Converting info...")
                info = convert_to_sonolus_info(course)
                with open(os.path.join(level_dir, "info.json"), "w") as f2:
                    json.dump(info, f2, indent=2)
                # Data
                if verbose:
                    print(f"[{course.slug}] Converting data...")
                data = convert_to_sonolus_data(course)
                with open(os.path.join(level_dir, "data.json"), "w") as f2:
                    json.dump(data, f2)
                # BGM
                if extract_bgm:
                    if verbose:
                        print(f"[{course.slug}] Copying bgm...")
                    shutil.copyfile(
                        bgm_dir,
                        os.path.join(level_dir, "bgm.mp3")
                    )
                # Cover
                if verbose:
                    print(f"[{course.slug}] Copying cover...")
                shutil.copyfile(
                    cover_path,
                    os.path.join(level_dir, "cover.png")
                )

                if verbose:
                    print(f"[{course.slug}] Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert TJA to Sonolus Taiko levels.'
    )
    parser.add_argument(
        '-o', '--output', help='Output directory.', default="out/"
    )
    parser.add_argument(
        '-c', "--cover", help='Path to cover image.'
    )
    parser.add_argument(
        '-x', "--extract-bgm", action="store_true", help='Extract bgm.'
    )
    parser.add_argument(
        '-v', "--verbose", action="store_true", help='Display messages.'
    )
    parser.add_argument(
        'input_dir', type=str, help='Folder containing TJA and OGG files.'
    )

    args = parser.parse_args()
    convert_level(
        args.input_dir,
        output_dir=args.output,
        cover_path=args.cover,
        extract_bgm=args.extract_bgm,
        verbose=args.verbose,
    )
