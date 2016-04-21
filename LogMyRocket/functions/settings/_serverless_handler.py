import os
import sys
os.environ['SERVERLESS_STAGE'] = str('dev')
os.environ['SERVERLESS_DATA_MODEL_STAGE'] = str('dev')
os.environ['SERVERLESS_PROJECT_NAME'] = str('LogMyRocket')
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(here)
from handler import handler