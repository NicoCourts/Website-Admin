import threading
import webview
import sys

from util.interface import APICaller

class Api:
    def __init__(self, is_dev):
        if is_dev:
            self.api_caller = APICaller("http://localhost:8080/")
        else:
            self.api_caller = APICaller()
        self.cancel_heavy_stuff_flag = False
        self.windows = []

    def add_window(self, window):
        self.windows.append(window)

    def close_program(self, trash):
        for window in self.windows:
            window.destroy()
        sys.exit(0)
    def get_posts(self, trash):
        print(self.api_caller.get_posts())


if __name__ == '__main__':
    is_dev = len(sys.argv) == 2 and sys.argv[1] == "--dev"

    api = Api(is_dev)
    window = webview.create_window('API example', url="static/main.html", js_api=api, frameless=False, resizable=True)
    #window2 = webview.create_window('two', html='test')
    api.add_window(window)
    #api.add_window(window2)
    webview.start(debug=True)