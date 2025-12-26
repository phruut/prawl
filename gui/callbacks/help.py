import webbrowser
import threading
from typing import Any

class HelpCallbacks:
    interface: Any
    update: Any

    def update_button(self):
        self.interface.configure('update_button', enabled=False)
        self.interface.configure('update_link', show=False)
        self.interface.set('update_status_text', 'checking for updates...')
        thread = threading.Thread(target=self.update_worker, daemon=True)
        thread.start()

    def update_worker(self):
        results = self.update.check()
        self.interface.queue_callback(lambda: self.update_post(None, None, results))

    def update_post(self, sender, app_data, user_data):
        message, is_update_available = user_data
        self.interface.set('update_status_text', message)
        if is_update_available and self.update.release_url:
            self.interface.configure(
                'update_link',
                show=True,
                label=f'download {self.update.latest_version}',
                callback=lambda: webbrowser.open(self.update.release_url)
            )
        self.interface.configure('update_button', enabled=True)
