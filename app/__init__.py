from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    print(url_for('/', values={id: 21}))
    return render_template('home.html')

if __name__ == "__main__":
    app.run()