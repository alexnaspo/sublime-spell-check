import sublime
import sublime_plugin
import sys
import os
# current solution to include the third party library pyenchant
sys.path.append(os.path.join(os.path.dirname(__file__), "pyenchant"))
import enchant

# @TODO multiple selection spell check


class SpellCheckerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit
        self.region = self.view.sel()

        phrase = self.view.substr(self.region[0])
        if not phrase:
            return  # nothing selected
        dictionary = enchant.Dict()
        self.suggestions = dictionary.suggest(phrase)
        if not dictionary.check(phrase):
            self.view.window().show_quick_panel(self.suggestions, self.replace, sublime.MONOSPACE_FONT)

    def replace(self, index):
        if (index == -1):
            return
        replacement = self.suggestions[index]
        self.view.replace(self.edit, self.region[0], replacement)
