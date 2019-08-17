import threading
import webview
import sys
import random

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

    def close_program(self, params):
        for window in self.windows:
            window.destroy()
        sys.exit(0)

    def get_posts(self, params):
        return self.api_caller.get_posts()

    def reset(self, params):
        return 0

    def toggle_visible(self, params):
        self.api_caller.toggle_visible(params)



if __name__ == '__main__':
    is_dev = len(sys.argv) == 2 and sys.argv[1] == "--dev"

    api = Api(is_dev)
    window = webview.create_window('API example', url="static/main.html", js_api=api, frameless=False, resizable=True)
    #window2 = webview.create_window('two', html='test')
    api.add_window(window)
    #api.add_window(window2)
    webview.start(debug=True)