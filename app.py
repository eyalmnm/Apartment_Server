from flask import Flask

app = Flask(__name__)


# Use BluePrint for extended abilities
# ************************************

if __name__ == '__main--':
    app.config
    # gallery.run()
    # You need to call gallery.run last, as it blocks execution of anything after it until the server is killed.
    # Preferably, use the flask run command instead.
    # Ref: https://github.com/pallets/flask/issues/2415
    app.run(debug=True, use_debugger=True, use_reloader=False, passthrough_errors=True)
