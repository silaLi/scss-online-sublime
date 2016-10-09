import sublime
import sublime_plugin
import urllib 
import json, shlex, os

class ScssonlimeCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		scss_size = self.view.size()
		scss = self.view.substr(sublime.Region(0, scss_size))
		payload = {
			"input": scss,
			"compiler": "3.4",
			"syntax": "scss",
			"original_syntax": "scss",
			"output_style": "expanded"
		}
		url = "http://www.sassmeister.com/app/3.4/compile"
		json_data = json.dumps(payload).encode('utf8');
		request = urllib.request.Request(url, data=json_data, method='POST', headers={'Content-Type': 'application/json'})
		opener = urllib.request.build_opener()
		response = opener.open(request)
		json_str = response.read().decode(encoding='utf-8', errors='strict')
		contents = json.loads(json_str)
		filename = self.view.file_name()

		new_css_file_name = filename+'.css'
		new_css = contents["css"]
		print(new_css_file_name)


		new_css_file_view = self.view.window().new_file()
		new_css_file_view.retarget(new_css_file_name)

		new_css_file_view = self.view.window().open_file(new_css_file_name)
		new_css_file_view.insert(edit, 0, new_css)
		new_css_file_view.set_encoding('css')
		new_css_file_view.run_command('save')

		return
		