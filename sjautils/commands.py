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

