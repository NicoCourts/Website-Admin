import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
import markdown as md

class UI:
    def __init__(self):
        self.window = EditorWindow()
        self.window.connect("destroy", Gtk.main_quit)

    def run(self):
        self.window.show_all()
        Gtk.main()

class EditorWindow(Gtk.Window):
    def __init__(self):
        # Initialize
        Gtk.Window.__init__(self, title="Placeholder Title")
        self.placeholder_text =  "Write your text here!"

        # set window properties
        self.set_default_size(1100, 900)
        self.paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        self.add(self.paned)

        # create elements
        self.text_v = TextEditor(placeholder=self.placeholder_text)
        self.web_v = WebPreview(placeholder=self.placeholder_text)

        # initialize the web view and attach panes to the window
        self.web_v.update_html(self.text_v.textbuffer)
        self.paned.add1(self.text_v)
        self.paned.add2(self.web_v)

        # Handle events
        self.text_v.textview.connect('key-release-event', self.on_key_release)
        self.text_v.textview.connect('focus-in-event', self.on_in_focus)
        self.text_v.textview.connect('focus-out-event', self.on_out_focus)

    def on_key_release(self, a, b):
        self.web_v.update_html(self.text_v.textbuffer)

    def on_out_focus(self, a, b):
        if self.text_v.textbuffer.get_char_count() == 0:
            self.text_v.textbuffer.set_text(self.placeholder_text)

    def on_in_focus(self, a, b):
        start, end = self.text_v.textbuffer.get_bounds()
        if self.text_v.textbuffer.get_text(start, end, True) == self.placeholder_text:
            self.text_v.textbuffer.set_text('')

class TextEditor(Gtk.ScrolledWindow):
    def __init__(self, placeholder):
        Gtk.ScrolledWindow.__init__(self)
        self.placeholder_text = placeholder
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_size_request(1100, 450)

        self.textview = Gtk.TextView()
        self.textview.set_top_margin(10)
        self.textview.set_bottom_margin(10)
        self.textview.set_right_margin(10)
        self.textview.set_left_margin(10)
        self.textview.set_wrap_mode(3)

        self.add(self.textview)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(self.placeholder_text)

class WebPreview(Gtk.ScrolledWindow):
    def __init__(self, placeholder):
        Gtk.ScrolledWindow.__init__(self)

        # Initialize text strings
        self.placeholder_text = placeholder
        with open('index.html', 'r') as f:
            self.html = f.read()
        with open('head.html', 'r') as f:
            self.head = f.read()
        with open('./styles.css', 'r') as f:
            lev = WebKit2.UserStyleLevel.USER
            fram = WebKit2.UserContentInjectedFrames.ALL_FRAMES
            self.style_sheet = WebKit2.UserStyleSheet.new(f.read(), fram, lev, None, None)
        
        self.ucm = WebKit2.UserContentManager.new()
        self.ucm.add_style_sheet(self.style_sheet)
        self.wk = WebKit2.WebView.new_with_user_content_manager(self.ucm)

        self.add(self.wk)
    
    def update_html(self, textbuffer):
        start, end = textbuffer.get_bounds()
        body =  textbuffer.get_text(start, end, True)
        body_html = self.mark_it_up(body)
        self.wk.load_html(self.html.format(
            head=self.head,
            title='Sample Post Title',
            date='Posted on August 24th, 1987',
            body_html=body_html))

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

if __name__=="__main__":
    interface = UI()
    interface.run()