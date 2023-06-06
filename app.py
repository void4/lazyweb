from flask import Flask, g


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    if hasattr(g, "_database"):
        g._database.close()
        del g._database
    return response
