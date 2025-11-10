import requests
import json

REPO_OWNER = 'phruut'
REPO_NAME = 'prawl'
API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest'

class Update:
    def __init__(self, version):
        self.api_url = API_URL
        self.current_version = version
        self.latest_version = None
        self.release_url = None

    def _version_parse(self, version):
        return tuple(map(int, version.split('.')))

    def check(self):
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()

            data = response.json()
            self.latest_version = data.get('tag_name')
            self.release_url = data.get('html_url')

            if not self.latest_version:
                return 'couldnt get latest version', False

            if self._version_parse(self.latest_version) > self._version_parse(self.current_version):
                return f'update available: {self.latest_version}', True
            elif self._version_parse(self.latest_version) == self._version_parse(self.current_version):
                return f'up to date! ({self.current_version})', False

        except requests.exceptions.RequestException:
            return 'could not connect to server', False
        except json.JSONDecodeError:
            return 'invalid response from server', False
        except Exception:
            return 'unexpected error occurred', False
