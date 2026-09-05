from flask import Flask, render_template

app = Flask(__name__)
app.config['secret_key'] = ''

@app.route('/')
def hello_world():
    return render_template("index.html", new="lol")

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)