import os, sys

os.environ['TESTING'] = "true"

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../libraries/user_libs"))

# Import functions tests
from unit.functions.login_test import *
