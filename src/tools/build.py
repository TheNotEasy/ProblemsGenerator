import os
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(f'{__file__}\\..\\..\\..')

DIST_DIR = BASE_DIR / 'dist'
SRC_DIR = BASE_DIR / 'src'
ASSETS_DIR = SRC_DIR / 'assets'

if not BASE_DIR.is_dir():
    raise NotADirectoryError("Base dir is not found, check the file structure")

shutil.rmtree(DIST_DIR, True)
shutil.rmtree(BASE_DIR / 'build', True)
os.chdir(BASE_DIR)

subprocess.run(
    ['pyinstaller', str(SRC_DIR / 'app.py'),
     '-F', '-w', '--icon', str(ASSETS_DIR / 'Icon.ico')]
)

shutil.copytree(SRC_DIR / 'assets', DIST_DIR / 'assets')
