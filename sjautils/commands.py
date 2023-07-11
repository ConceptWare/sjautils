from sjautils.subprocess_utils import command_out_err
import os, shutil

def unrar(path, remove_after=True):
    cmd = f'rar x {path}'
    out,err = command_out_err(cmd)
    if err:
        raise Exception(f'{cmd}: err')
    elif remove_after:
        os.remove(path)

