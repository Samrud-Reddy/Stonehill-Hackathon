import subprocess

def convert_mp3_to_webm(input_file, output_file, bitrate="128k"):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-c:a", "libopus",
        "-b:a", bitrate,
        output_file
    ]
    subprocess.run(command, check=True)
