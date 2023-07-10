from sjautils.subprocess_utils import command_out_err
import os, shutil

def unrar(path):
    cmd = f'rar x {path}'
    out,err = command_out_err(cmd)
    if err:
        print(f'{cmd}: err')
    else:
        os.remove(path)
