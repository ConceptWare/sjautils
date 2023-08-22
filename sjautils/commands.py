from sjautils.subprocess_utils import command_out_err
import os, shutil

def unrar(path, remove_after=True):
    if ' ' in path:
        path = '"' + path + '"'
    cmd = f'unrar x {path}'
    out,err = command_out_err(cmd)
    if err and not out:
        raise Exception(f'{cmd}: {err}')
    elif remove_after:
        os.remove(path)

def transcribe(path, delete_download=False, json_out=None):
    pass

sample_dlp = """
 yt-dlp "https://odysee.com/@MarkMoss:7/why-aren't-the-markets-crashing:b"
[lbry] Extracting URL: https://odysee.com/@MarkMoss:7/why-aren't-the-markets-crashing:b
[lbry] @MarkMoss#7/why-aren't-the-markets-crashing#b: Downloading stream JSON metadata
[lbry] b598f8b414784a79bdb7ee412bb20f6377a5d9d2: Downloading streaming url JSON metadata
[lbry] @MarkMoss#7/why-aren't-the-markets-crashing#b: Checking for original quality
[lbry] @MarkMoss#7/why-aren't-the-markets-crashing#b: Downloading streaming redirect url info
[lbry] @MarkMoss#7/why-aren't-the-markets-crashing#b: Downloading m3u8 information
[info] b598f8b414784a79bdb7ee412bb20f6377a5d9d2: Downloading 1 format(s): original
[download] Destination: Why Aren't the Markets Crashing - Quarterly Report [b598f8b414784a79bdb7ee412bb20f6377a5d9d2].mp4
[download] 100% of  543.61MiB in 00:00:17 at 30.66MiB/s

"""

def download_video(vurl):
    cmd = f'yt-dlp {vurl}'
    out, err = comand_out_err(cmd)
    if not err:
        for l in out:
            if 'Destination:' in out:
                fname = after(l, 'Destination:')
                return fname
    else:
        raise Exception(f'problem downloading {err}')
