import requests
import json

class Update:
    def __init__(self, config):
        self.config = config
        self.api_url = f'https://api.github.com/repos/{self.config.network.repo_owner}/{self.config.network.repo_name}/releases/latest'
        self.current_version = config.version
        self.latest_version = None
        self.release_url = None

    def _version_parse(self, version):
        # i forgot where i got this off from
        return tuple(map(int, version.split('.')))

    def check(self, callback=None):
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()

            data = response.json()
            self.latest_version = data.get('tag_name')
            self.release_url = data.get('html_url')

            if not self.latest_version:
                result = 'couldnt get latest version', False
            elif self._version_parse(self.latest_version) > self._version_parse(self.current_version):
                result = f'update available: {self.latest_version}', True
            elif self._version_parse(self.latest_version) == self._version_parse(self.current_version):
                result = f'up to date! ({self.current_version})', False
            else:
                result = f'mystery version :o ({self.current_version})', False

        except requests.exceptions.RequestException:
            result = 'could not connect to server', False
        except json.JSONDecodeError:
            result = 'invalid response from server', False
        except Exception:
            result = 'unexpected error occurred', False

        if callback:
            callback(result)
        return result
