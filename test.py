"""The main entry point for the program."""
import webview
import iso8601 as iso
from util.interface import APICaller

class Api:
    """Provides an API for Javascript to communicate with Python"""
    def __init__(self):
        self.site = APICaller()

    def go_to(self, target):
        """Navigates to the given (local) page."""
        with open('static/'+target+'.html', "r") as f:
            webview.load_html(f.read())

    def get_posts(self, trash):
        """Pulls post data from the nicocourts API. I don't know why it sends an extra variable."""
        posts = self.site.get_posts()
        html = "<table style='width:100%'><tr><th>Post Title</th><th>Post Type</th>" + \
            "<th>Posted</th><th>Visible</th></tr>"
        for post in posts:
            if post['isshort']:
                posttype = 'Short'
            else:
                posttype = 'Long'

            date_string = iso.parse_date(post['date'])
            my_str = "<tr><td>{title}</td><td>{type}</td><td>{date}</td><td>{visible}</td></tr>"
            html += my_str.format(title=post['title'],
                                  type=posttype,
                                  date=date_string.strftime("%A, %d %B %Y %I:%M%p"),
                                  visible=post['visible'])

        html += "</table>"
        return html

    def test(self, trash):
        """Just testing."""
        print(self.site.get_nonce())

if __name__ == '__main__':
    API = Api()
    webview.create_window('Talking to Javascript', 'static/main.html', js_api=API, debug=False)
