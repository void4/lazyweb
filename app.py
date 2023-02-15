from flask import Flask

class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
		variable_end_string='%%',
	))

app = CustomFlask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
