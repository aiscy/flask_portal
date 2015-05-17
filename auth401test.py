__author__ = 'Maxim'
from flask import Flask, render_template_string, abort, Response, request
app = Flask(__name__)

@app.route('/')
def index():
    print(request.environ.get('REMOTE_USER'))
    abort(401)
    return render_template_string('<!doctype html>'
                                  'Test!')



@app.errorhandler(401)
def custom_401(error):
    return Response('HTTP/1.0 401 Unauthorized', 401, {'WWW-Authenticate: NTLM'})



app.run()