
import os
from os.path import expanduser


import sys


def get_firefox_profile_dir():

    FF_PRF_DIR_DEFAULT = ""

    if sys.platform in ['linux', 'linux2']:
        import subprocess
        cmd = "ls -d /home/$USER/.mozilla/firefox/*.default/"
        p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
        FF_PRF_DIR = p.communicate()[0][0:-2]
        FF_PRF_DIR_DEFAULT = str(FF_PRF_DIR, 'utf-8')
    elif sys.platform == 'win32':
        import os
        import glob
        APPDATA = os.getenv('APPDATA')
        FF_PRF_DIR = "%s\\Mozilla\\Firefox\\Profiles\\" % APPDATA
        PATTERN = FF_PRF_DIR + "*default*"
        FF_PRF_DIR_DEFAULT = glob.glob(PATTERN)[0]

    return FF_PRF_DIR_DEFAULT


if __name__ == "__main__":
    print(get_firefox_profile_dir())
