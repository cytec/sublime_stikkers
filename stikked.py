import sublime, sublime_plugin
import os, urllib, re

class stikked(sublime_plugin.TextCommand):
	#Run when plugin starts
	def run(self, edit, **args):

		#Load the user's settings
		s = sublime.load_settings('Stikked.sublime-settings')
		author = s.get("author")
		url = s.get("url")

		#Get the censored view of our current file
		if self.view.sel()[0].begin() != self.view.sel()[0].end():
                        text = ""
                        for region in self.view.sel():
                                text = text + self.view.substr(region)
                else:
                        text = self.get_text()

		data = urllib.urlencode( {"title":self.cur_file(), "text":text, "name":author, "lang":self.cur_syntax() } )
			
		#Encode and send out data
		u = urllib.urlopen(url, data)

		#Set the url to the clipboard
		sublime.set_clipboard(u.read())

	#Get the syntax of the current file
	def cur_syntax(self):
		syntax = self.view.settings().get('syntax')
		syntax = syntax.split("/", 2)
		return syntax[1]

	#Return the name of the file without the path
	def cur_file(self):
		return os.path.basename(self.view.file_name())

	def get_text(self):
		text = self.view.substr(sublime.Region(0, self.view.size()))
		to_kill = sublime.load_settings('Stikked.sublime-settings').get("kill")
		#to_rep  = sublime.load_settings('Stikked.sublime-settings').get("replace")
		
		for rage in to_kill:
			text = re.sub(rage[0], rage[1], text)
		
		return text
