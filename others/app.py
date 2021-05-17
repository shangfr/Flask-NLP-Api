from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "欢迎使用 CODING 代码模板"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')    