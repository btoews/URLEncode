import sublime
import sublime_plugin
import urllib

class UrlencodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """
        Main plugin logic for the 'urlencode' command.
        """
        view = self.view
        regions = view.sel()
        # if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
                for region in view.sel():
                    if not region.empty():
                        s = view.substr(region)
                        s = urllib.quote(s)
                        view.replace(edit, region, s)
        else:   #format all text
                alltextreg = sublime.Region(0, view.size())
                s = view.substr(alltextreg)
                s = urllib.quote(s)
                view.replace(edit, alltextreg, s)


class UrldecodeCommand(sublime_plugin.TextCommand):

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
                        s = view.substr(region)
                        s = urllib.unquote(s)
                        view.replace(edit, region, s)
        else:   #format all text
                alltextreg = sublime.Region(0, view.size())
                s = view.substr(alltextreg)
                s = urllib.unquote(s)
                view.replace(edit, alltextreg, s)