""" Main entry point for the program"""
import html
import os
import sys
import markdown
import webview
import json

from jinja2 import Template
from util.interface import APICaller

class Api:
    """API to communicate with the GUI"""
    def __init__(self, is_dev):
        if is_dev:
            self.api_caller = APICaller("http://localhost:8080/")
        else:
            self.api_caller = APICaller()
        self.cancel_heavy_stuff_flag = False
        self.posts = []
        self.main_window = 0

    def set_main_window(self, win):
        """Keep hold of that main window!"""
        self.main_window = win

    def close_program(self, params):
        """Close!"""
        self.main_window.destroy()
        sys.exit(0)

    def get_posts(self, params):
        """Query the web API for the current posts"""
        self.posts = self.api_caller.get_posts()
        return self.posts

    def get_post(self, postid):
        """Get the info for the post with a given id"""
        if self.posts == []:
            self.get_posts(0)
        for post in self.posts:
            if str(post['_id']) == postid[1:]:
                return post
        return {}

    def edit_post(self, postid):
        """Grab post parameters and navigate the main window to the editing page"""
        post = self.get_post(postid)
        with open('static/post-edit.html', 'r') as f:
            template = Template(f.read())
        html = template.render(
            title=post['title'],
            body=json.loads(post['markdown']),
            new_post='false',
            postid=post['_id']
        )
        with open('static/post-edit-live.html', 'w') as f:
            f.write(html)
        self.go_to('post-edit-live')

    def edit_new_post(self, params):
        """Create a new post and open it for editing"""
        with open('static/post-edit.html', 'r') as f:
            template = Template(f.read())
        html = template.render(
            title='',
            body='',
            new_post='true',
            postid=0
        )
        with open('static/post-edit-live.html', 'w') as f:
            f.write(html)
        self.go_to('post-edit-live')

    def reset(self, params):
        """Pywebview isn't letting me make repeated calls to the same API point
        so I made this function as a workaround. Seems like a huge oversight to me."""
        return 0

    def toggle_visible(self, params):
        """Toggle the visibility of the post with id param"""
        self.api_caller.toggle_visible(params)

    def go_to(self, page):
        """Navigate the main window to the given filename"""
        base_url = os.path.dirname(os.path.abspath(__file__))
        self.main_window.load_url('file://' + base_url + '/static/' + page + '.html')

    def submit(self, params):
        """Submits a post to the API"""
        # Determine whether this is an update to an existing post
        post = {'title': params[2], 'markdown': json.dumps(params[3]), 'body': json.dumps(markitdown(params[3]))}
        if params[0]:
            #new post
            self.api_caller.create_post(post)
        else:
            #update
            self.api_caller.update_post(post, params[1])

    def preview(self, parts):
        """Open a preview window containing the current parts"""
        title = parts[0]
        date = parts[1]
        body = markitdown(parts[2])
        with open('static/index.html', 'r') as f:
            template = Template(f.read())
        html = template.render(title=title, date=date, body_html=body)
        with open('static/index-full.html', 'w') as f:
            f.write(html)

        webview.create_window(
            'Preview',
            url='static/index-full.html',
            width=1024,
            height=800,
            frameless=False,
            resizable=False
        )

def markitdown(txt):
    """Helper function to convert markdown with LaTeX to HTML"""
    extension_configs = {
        'mdx_math': {'enable_dollar_delimiter': True}
    }
    md = markdown.Markdown(extensions=['mdx_math'], extension_configs=extension_configs)
    return md.convert(txt)

if __name__ == '__main__':
    IS_DEV = len(sys.argv) == 2 and sys.argv[1] == "--dev"

    API = Api(IS_DEV)
    WINDOW = webview.create_window(
        'Post Administration',
        url="static/main.html",
        js_api=API,
        width=1024,
        height=800,
        frameless=False,
        resizable=False
    )

    API.set_main_window(WINDOW)
    webview.start(debug=True)
