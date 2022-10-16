from flask import Flask, render_template
import hello

application = Flask(__name__)
@application.route('/')
def index():
    return hello.hello('AWS EB')

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)