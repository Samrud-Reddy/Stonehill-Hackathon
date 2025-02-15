import os

def convert_mp3_to_webm(input_file, bitrate="128k"):
    output_file = input_file.split(".")[0]+".webm"
    print(input_file)
    print(output_file)
    cmd = f"ffmpeg -i {input_file} {output_file} -y"
    print(cmd)
    os.system(cmd)
    os.remove(input_file)
