#!/usr/bin/python
import os
import sys
import site
import logging
logging.basicConfig(stream=sys.stderr)

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/ox/pedestal/pedweb_venv/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/ox/pedestal/web/pedestal_web/')

# Activate your virtual env
activate_env=os.path.expanduser("/home/ox/pedestal/pedweb_venv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from app import app as application
#application.secret_key = 'Flask-py-susbscription-appp~#@)(*&!'

