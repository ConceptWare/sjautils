from cwutils.tools import DictObject
import json, os
import yaml

class Environment(DictObject):
  def __init__(self):
    defaults = dict(
      PYTHON_AIRBRAKE_PROJECT_ENV = 'stage',
      PYTHON_AIRBRAKE_PROJECT_ID = '219081',
      PYTHON_AIRBRAKE_PROJECT_KEY='1c722767e36562df001dc8c87bf56453',
      DEFAULT_LANG='en',
      NAMED_ENV='dev',
      ENVIRONMENT='dev',
      SEGMENT_WRITE_KEY='KOGKqAin2rhjMvqVXdjxJ8a24eaA85k2',
      ALLOW_USER_INVITES_DEFAULT=True,
      ALLOW_USER_SIGNUP_DEFAULT = True,
      ALLOW_GROUP_CREATION_DEFAULT = True,
      ALLOW_GROUP_DISCOVERY_DEFAULT = True,
      DEPARTMENTS_IN_SIGNUP_DEFAULT = False,
      DEPARTMENTS_IN_SIGNUP_REQUIRED_DEFAULT = False,
      LOCATIONS_IN_SIGNUP_DEFAULT = False,
      LOCATIONS_IN_SIGNUP_REQUIRED_DEFAULT = False,
      SUPPORT_MULTIPLE_LANGUAGES_DEFAULT = False,
      POLICY_BASE_URL = os.environ.get('POLICY_BASE_URL', 'baseurl'),
      REPORTS_BUCKET='esreportsdev'
    )
    super().__init__(**defaults)

  def find_env(self):
    start = os.path.dirname(__file__)

    while os.path.basename(start) != 'python_common':
      start = os.path.dirname(start)
    path = os.path.join('')

  def read_env(self, env_path='', env='dev'):
    if not env_path:
      env_path = os.path.join(os.path.dirname(__file__), 'aws_env.yml')
    if env_path:
      if os.path.exists(env_path):
        with open(env_path) as f:
          data = yaml.load(f, Loader=yaml.FullLoader)
          for k,v in data.get(env, {}).items():
            self[k] = v


our_env = Environment()

def read_env(env_path='', env='dev'):
  our_env.read_env(env_path, env)

def set_current_env(env=None, aws_profile=None, **kwargs):
  if aws_profile:
    set_env('aws_profile', aws_profile)
  if env:
    read_env(env=env)
  for k,v in kwargs:
    set_env(k, v)

def get_env(key, default=None, translate=True):
  '''
  Returns the value of key in the current environment.
  Let the os.environ value if any overrule what is stored and store it if present.
  Else return the stored value if present.  Else store and return the default
  if provided.
  :param: key - environment variable name
  :param: default - default value if not present
  :returns: the value associated with key or None
  '''

  val = os.environ.get(key)
  if val:
    our_env[key] = val
  elif key not in our_env:
    if default is not None:
      our_env[key] = default
  raw = our_env.get(key)
  if raw and translate:
    try:
      return json.loads(raw)
    except:
      pass
  return raw

def set_env(key, val):
  if isinstance(val, dict):
    val = json.dumps(val)
  elif isinstance(val, bool):
    val = json.dumps(val)
  elif isinstance(val, str):
    val = json.dumps(val)
  else:
    val = str(val)
  os.environ[key] = val

