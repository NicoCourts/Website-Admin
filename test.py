import webview
import datetime
import iso8601 as iso
from util.interface import APICaller

class Api:
    def __init__(self):
        self.site = APICaller()

    def goTo(self, target):
        with open('static/'+target+'.html', "r") as f:
            webview.load_html(f.read())
    
    def get_posts(self, arg):
        posts = self.site.get_posts()
        html = "<table style='width:100%'><tr><th>Post Title</th><th>Post Type</th><th>Posted</th><th>Visible</th></tr>"
        for post in posts:
            if post['isshort']:
                posttype = 'Short'
            else:
                posttype = 'Long'

            d = iso.parse_date(post['date'])
            html += "<tr><td>{title}</td><td>{type}</td><td>{date}</td><td>{visible}</td></tr>".format(title=post['title'],
                        type = posttype,
                        date = d.strftime("%A, %d %B %Y %I:%M%p"),
                        visible = post['visible'])

        html += "</table>"
        return html

if __name__ == '__main__':
    api = Api()
    webview.create_window('API example', 'static/main.html', js_api=api, debug=True)
