import threading
import webview
import sys

class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False
        self.windows = []

    def add_window(self, window):
        self.windows.append(window)

    def close_program(self, trash):
        for window in self.windows:
            window.destroy()
        sys.exit(0)
    def print(self, trash):
        print("YAY")


if __name__ == '__main__':
    api = Api()
    window = webview.create_window('API example', url="static/main.html", js_api=api, frameless=True)
    #window2 = webview.create_window('two', html='test')
    api.add_window(window)
    #api.add_window(window2)
    webview.start(debug=True)