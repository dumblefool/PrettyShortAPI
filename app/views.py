from flask import jsonify
from app import app
import PrettyShort

@app.route('/')
@app.route('/index')
def index():
        output=PrettyShort.prest()
        return jsonify(**output)
