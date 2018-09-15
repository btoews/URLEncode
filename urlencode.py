import sublime
import sublime_plugin
import urllib


def get_current_encoding(view, default='utf8'):
    """Get the encoding of view, else return default
    """
    view_encoding = view.encoding()
    if view_encoding == 'Undefined':
        view_encoding = view.settings().get('default_encoding', default)

    br1 = view_encoding.find('(')
    br2 = view_encoding.find(')')
    if br2 > br1:
        view_encoding = view_encoding[br1+1:br2].replace(' ', '-')

    return view_encoding


def updateSelection(self, edit, command):
    view = self.view
    selection = view.sel()
    for region in selection:
        if region.empty():
            continue

        s = view.substr(region)

        if command == 'encode':
            view.replace(edit, region, quote(view, s))
        elif command == 'decode':
            view.replace(edit, region, unquote(view, s))

        # update coords so next regions get shifted and still refer the correct buffer positions
        region.b = region.a + len(s)


ST3 = sublime.version() == '' or int(sublime.version()) > 3000

if ST3:

    def quote(view, s):
        return urllib.parse.quote(s, safe='')

    def unquote(view, s):
        return urllib.parse.unquote(s)

else:
    # py26 urllib does not quote unicode, so encode first

    def quote(view, s):
        enc = get_current_encoding(view)
        return urllib.quote(s.encode(enc), safe='')

    def unquote(view, s):
        settings = sublime.load_settings('URLEncode.sublime-settings')
        fallback_encodings = settings.get('fallback_encodings', [])
        fallback_encodings.insert(0, get_current_encoding(view))

        s = urllib.unquote(s.encode('utf8'))

        ## Now decode (to unicode) using best guess encoding
        for enc in fallback_encodings:
            try:
                return s.decode(enc)
            except UnicodeDecodeError:
                continue
        return s


class UrlencodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        updateSelection(self, edit, 'encode')

class UrldecodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        updateSelection(self, edit, 'decode')
