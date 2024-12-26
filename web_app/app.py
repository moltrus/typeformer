from flask import Flask, request, render_template
import json
import server

app = Flask(__name__)


@app.route('/')
def index():
    print("Index page rendered")
    return render_template('index.html')


@app.route('/segcorrect', methods=['post'])
def segcorrect():
    print("Segcorrect")
    try:
        user_input = ''.join(request.json['input_text'].split())
        res = server.request_server(model="gemma2:2b", stream=False, task="segncorrect", data=user_input)
        print(res)
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    except Exception as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')


@app.route('/predict', methods=['post'])
def predict():
    print("Got post")
    print(request.json)
    try:
        user_input = ''.join(request.json['input_text'].split())
        top_k = request.json['top_k']
        res = server.request_server(model="gemma2:2b", stream=False, task="predict", data=user_input, n=top_k)
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    except OSError as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=True)
