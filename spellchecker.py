import sublime
import sublime_plugin
# current solution to include the third party library PyEnchant
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "pyenchant"))
import enchant


class SpellCheckerCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
        self.selection = view.sel()
        self.dictionary = enchant.Dict()

    def run(self, edit):
        self.edit = edit
        phrase = self.view.substr(self.selection[0])
        if not phrase:
            return  # nothing selected
        self.suggestions = self.dictionary.suggest(phrase)

        if not self.dictionary.check(phrase):
            self.view.window().show_quick_panel(self.suggestions, self.replace, sublime.MONOSPACE_FONT)
        else:
            sublime.status_message(phrase + " is spelled correctly")

    def replace(self, index):
        if (index == -1):
            return
        self.view.replace(self.edit, self.selection[0], self.suggestions[index])
