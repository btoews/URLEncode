import sublime
import sublime_plugin
import urllib

SETTINGS = sublime.load_settings('URLEncode.sublime-settings')

def get_current_encoding(view):

    view_encoding = view.encoding()
    if view_encoding == 'Undefined':
        view_encoding = view.settings().get('default_encoding', 'UTF-8')

    br1 = view_encoding.find('(')
    br2 = view_encoding.find(')')
    if br2 > br1:
        view_encoding = view_encoding[br1+1:br2].replace(' ', '-')

    return view_encoding


class UrlencodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """
        Main plugin logic for the 'urlencode' command.
        """
        view = self.view
        regions = view.sel()
        # if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
                current_encoding = get_current_encoding(self.view)
                for region in view.sel():
                    if not region.empty():
                        s = view.substr(region).encode(current_encoding)
                        s = urllib.quote(s)
                        view.replace(edit, region, s)
        else:   #format all text
                alltextreg = sublime.Region(0, view.size())
                s = view.substr(alltextreg).encode(get_current_encoding(self.view))
                s = urllib.quote(s)
                view.replace(edit, alltextreg, s)


class UrldecodeCommand(sublime_plugin.TextCommand):

    def utf8_encode_with_fallback_encodings(self, s):
        """
        Try different encodings
        """
        encodings_to_try = SETTINGS.get('fallback_encodings', [])
        view_encoding = get_current_encoding(self.view)

        encodings_to_try.insert(0, view_encoding)

        result = s
        for enc in encodings_to_try:
            try:
                result = unicode(s, enc)
                break
            except UnicodeDecodeError:
                pass

        return result


    def run(self, edit):
        """
        Main plugin logic for the 'urldecode' command.
        """
        view = self.view
        regions = view.sel()
        # if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
                for region in view.sel():
                    if not region.empty():
                        s = view.substr(region).encode('utf-8')
                        s = self.utf8_encode_with_fallback_encodings(urllib.unquote(s))
                        view.replace(edit, region, s)
        else:   #format all text
                alltextreg = sublime.Region(0, view.size())
                s = view.substr(alltextreg).encode('utf-8')
                s = self.utf8_encode_with_fallback_encodings(urllib.unquote(s))
                view.replace(edit, alltextreg, s)