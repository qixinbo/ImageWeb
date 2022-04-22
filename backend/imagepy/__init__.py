import os.path as osp
root_dir = osp.abspath(osp.dirname(__file__))

import sys
sys.path.append('../')
from imagepy.app import startup
startup.start()