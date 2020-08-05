#! /usr/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/vdelaluz/git/Sistemas-Distribuidos/www')
from twitrends import app as application
application.secret_key = 'seguramentenoesgalimatias'
