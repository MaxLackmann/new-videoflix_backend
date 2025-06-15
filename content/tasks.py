import subprocess

def convert_120p(source):
    target = source.replace(".mp4", "_120p.mp4")
    cmd = 'ffmpeg -i "{}" -vf scale=-2:120 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)

def convert_480p(source):
    target = source.replace(".mp4", "_480p.mp4")
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)

def convert_720p(source):
    target = source.replace(".mp4", "_720p.mp4")
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)

def convert_1080p(source):
    target = source.replace(".mp4", "_1080p.mp4")
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)