import django_rq
import subprocess

@django_rq.job
def convert_120p(source: str) -> None:
    target = source.replace(".mp4", "_120p.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-vf", "scale=-2:120",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-strict", "-2",
        target,
    ]
    subprocess.run(cmd, check=True)

@django_rq.job
def convert_480p(source: str) -> None:
    target = source.replace(".mp4", "_480p.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-vf", "scale=-2:480",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-strict", "-2",
        target,
    ]
    subprocess.run(cmd, check=True)

@django_rq.job
def convert_720p(source: str) -> None:
    target = source.replace(".mp4", "_720p.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-vf", "scale=-2:720",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-strict", "-2",
        target,
    ]
    subprocess.run(cmd, check=True)

@django_rq.job
def convert_1080p(source: str) -> None:
    target = source.replace(".mp4", "_1080p.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-vf", "scale=-2:1080",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-strict", "-2",
        target,
    ]
    subprocess.run(cmd, check=True)
