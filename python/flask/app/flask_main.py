from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    ans = {'message':'hello'}
    return jsonify(ans)
    
@app.route('/health', methods=['GET'])
def health():
    return 'OK'
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)