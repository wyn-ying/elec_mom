from flask import Flask, request, jsonify
from flask_cors import CORS
from alitts import run_once

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logger = app.logger

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    content = request.form['content']
    voiceid = request.form.get('voiceid')
    print(title, content, voiceid)
    run_once(content, title)
    return f"./music/eleven/{title}.mp3"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8124)
