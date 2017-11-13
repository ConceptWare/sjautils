import requests

class WebInterface(object):
  '''
  Purpose of this class is to provide restful calls to a webserver.  
  There are common patterns to consider including handling CSRF issues.
  Subclasses can specialize as needed or provide extra methods wrapping restful
  calls.
  '''
  def __init__(self, main_url, base_get, csrf_key='csrftoken'):
    '''
    General interaction with a single webserver across restful calls.
    :param main_url: the base url for getting to the webserver without trailing slash
    :param base_get: a GET target used only to obtain a csrf cookie from the server
    :param csrf_key: the cookie key the webserver uses for csrf return.  It can vary
    depending on type of server.  Here it is preset appropriately for DJANGO. 
    '''
    self._main_url = main_url
    self._session = requests.Session()
    self._csrf_key = csrf_key

  def _get_csrf(self, response):
    '''
    Gets the csrf token from a response.  Different backends 
    use different keys for that cookie.  Many types of backends
    require the csrf cookie to do a write method operations such as POST.
    
    :param response: the response to get the cookie from
    :return: 
    '''
    return response.cookies.get(self._csrf_key)

  def _setup_headers(self, base_get):
    response = self.get(base_get)
    self._session.headers['X-CSRFToken'] = self._get_csrf(response)

  def get(self, target, **query_params):
    return self._session.get(self.make_url(target), params=query_params)

  def make_url(self, target):
    return '/'.join([self._main_url, target])

  def post(self, target, json_data):
    url = self.make_url(target)
    return self._session.post(url, json=json_data)

  
