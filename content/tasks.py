import os
import django_rq
import subprocess

@django_rq.job
def convert_480p(source: str) -> None:
    """
    Encode a video to 480p resolution using FFmpeg and H.264 video and AAC audio.
    :param source: Path to the video file to be encoded.
    :return: None
    """

    outdir = source.replace('.mp4', '_480p')
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "index.m3u8")
    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-vf", "scale=-2:480",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-strict", "-2",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(outdir, "segment_%03d.ts"),
        target
    ]
    subprocess.run(cmd, check=True)

@django_rq.job
def convert_720p(source: str) -> None:
    """
    Encode a video to 720p resolution using FFmpeg and H.264 video and AAC audio.
    :param source: Path to the video file to be encoded.
    :return: None
    """
    outdir = source.replace('.mp4', '_720p')
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "index.m3u8")
    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-vf", "scale=-2:720",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-strict", "-2",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(outdir, "segment_%03d.ts"),
        target
    ]
    subprocess.run(cmd, check=True)

@django_rq.job
def convert_1080p(source: str) -> None:
    """
    Encode a video to 1080p resolution using FFmpeg and H.264 video and AAC audio.
    :param source: Path to the video file to be encoded.
    :return: None
    """
    
    outdir = source.replace('.mp4', '_1080p')
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "index.m3u8")
    cmd = [
        "ffmpeg", "-y", "-i", source,
        "-vf", "scale=-2:1080",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-strict", "-2",
        "-f", "hls",
        "-hls_time", "6",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", os.path.join(outdir, "segment_%03d.ts"),
        target
    ]
    subprocess.run(cmd, check=True)