import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
import markdown as md

class UI:
    def __init__(self, config = dict()):
        self.config = config
        self.window = MainWindow(self.config)
        self.window.connect("destroy", Gtk.main_quit)
        self.run()

    def run(self):
        self.window.show_all()
        Gtk.main()

class MainWindow(Gtk.Window):
    def __init__(self, config = dict()):
        Gtk.Window.__init__(self, title="Testing stuff")
        self.set_default_size(900, 1100)
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Initialize text strings
        self.placeholder_text = "Write your text here!"
        with open('index.html', 'r') as f:
            self.html = f.read()
        with open('head.html', 'r') as f:
            self.head = f.read()
        
        # Create the elements
        self.create_textview()
    
    def create_textview(self):
        self.paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        self.grid.attach(self.paned, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textview.set_top_margin(10)
        self.textview.set_bottom_margin(10)
        self.textview.set_right_margin(10)
        self.textview.set_left_margin(10)
        self.textview.set_wrap_mode(3)

        with open('./styles.css', 'r') as f:
            lev = WebKit2.UserStyleLevel.USER
            fram = WebKit2.UserContentInjectedFrames.ALL_FRAMES
            self.style_sheet = WebKit2.UserStyleSheet.new(f.read(), fram, lev, None, None)
        self.ucm = WebKit2.UserContentManager.new()
        self.ucm.add_style_sheet(self.style_sheet)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(self.placeholder_text)

        self.win = Gtk.ScrolledWindow()
        self.win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.win.set_hexpand(True)
        self.win.set_vexpand(True)
        self.win.set_size_request(900, 450)
        self.win.add(self.textview)

        self.paned.add1(self.win)

        self.wk = WebKit2.WebView.new_with_user_content_manager(self.ucm)
        self.paned.add2(self.wk)
        self.update_html()

        self.textview.connect('key-release-event', self.on_key_release)
        self.textview.connect('focus-in-event', self.on_in_focus)
        self.textview.connect('focus-out-event', self.on_out_focus)

    def on_key_release(self, widget, event):
        self.update_html()

    def on_out_focus(self, event, what):
        if self.textbuffer.get_char_count() == 0:
            self.textbuffer.set_text(self.placeholder_text)

    def on_in_focus(self, event, what):
        start, end = self.textbuffer.get_bounds()
        if self.textbuffer.get_text(start, end, True) == self.placeholder_text:
            self.textbuffer.set_text('')

    def update_html(self):
        start, end = self.textbuffer.get_bounds()
        body =  self.textbuffer.get_text(start, end, True)
        body_html = self.mark_it_up(body)
        #print(body_html)
        self.wk.load_html(self.html.format(head=self.head, title='Sample Post Title', date='Posted on August 24th, 1987', body_html=body_html))

    def mark_it_up(self, mdn):
        exts = ['codehilite',
                'sane_lists',
                'extra',
                'admonition',
                'mdx_math']
        cfgs = {'mdx_math' : {'enable_dollar_delimiter' : True,
                              'add_preview' : True},
                'codehilite' : {'noclasses' : True,
                                'pygments_style' : 'perldoc'}
             }
        return md.markdown(mdn, extensions=exts, extension_configs=cfgs)

class PostEditor(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.navbar = Gtk.HBox()
        self.tabs = Gtk.Notebook()

        wk = WebKit2.WebView()
        self.tabs.prepend_page(wk)
        wk.load_uri('http://www.google.com')

        self.tabs.show_all()
        self.add(self.navbar)
        self.add(self.tabs)

config = {'title': 'Test program ...'}
x = UI(config)