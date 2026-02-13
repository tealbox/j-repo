import requests
from base64 import b64encode
from functools import wraps

# Custom exception
class AuthenticationError(Exception):
    """Raised when NSX session is not authenticated."""
    pass

def requires_auth(func):
    """Decorator to ensure the NSX instance is authenticated before calling the method."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Check if 'token' exists and is non-empty
        if not getattr(self, 'token', None):
            # Optionally auto-login if credentials are available
            if hasattr(self, 'login'):
                self.login()
            else:
                raise AuthenticationError("Authentication required but no login method or token found.")
        return func(self, *args, **kwargs)
    return wrapper


class myNSX:
    def __init__(self, nsxmgr, username="admin", password="VMware1!VMware1!"):
        self.s = requests.Session()
        self.hostname = nsxmgr
        self.username = username
        self.password = password
        self.s.verify = False  # Disable SSL warnings (use cautiously!)
        requests.packages.urllib3.disable_warnings()  # Optional: suppress InsecureRequestWarning

        cred = self.getEncoded()
        self.headers = {
            'Accept-Encoding': 'gzip',
            'Content-Type': "application/json",
            'Accept': 'application/json',
            'Authorization': f'Basic {cred}'
        }
        self.baseUrl = f"https://{self.hostname}/policy/api/v1"
        self.token = None  # Will be set after login

    def getEncoded(self):
        s = f'{self.username}:{self.password}'.encode('utf-8')
        return b64encode(s).decode('utf-8')

    def __do(self, method="GET", api="", payload=None, name=None, domain_id="default"):
        if payload is None:
            payload = {}

        if 'https' in api:
            url = api
        elif "/policy/api/v1/" in api:
            url = f"https://{self.hostname}/{api}"
        else:
            url = f"{self.baseUrl}{api}"

        # Use the current headers (may include token later)
        headers = self.headers.copy()
        if self.token:
            headers['Authorization'] = f"Bearer {self.token}"

        try:
            response = self.s.request(
                method=method.upper(),
                url=url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API call failed: {e}")
            return None

    def login(self):
        """Perform login and store token."""
        api = "/infra/login"
        res = self.__do(method="POST", api=api, payload={})
        if res and "token" in res:
            self.token = res["token"]
            # Update headers to use Bearer token for future calls
            self.headers['Authorization'] = f"Bearer {self.token}"
        else:
            raise AuthenticationError("Login failed: No token returned.")

    @requires_auth
    def get_services(self):
        api = "/infra/services"
        res = self.__do(method="GET", api=api)
        if res and "results" in res:
            self.all_services = res['results']
            return self.all_services
        return None
