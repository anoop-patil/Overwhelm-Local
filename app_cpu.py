from flask import Flask, request

app = Flask(__name__)


@app.route('/cpu-overload', methods=['GET'])
def cpu_overload():
    iterations = int(request.args.get('iterations', 1000000))

    total = 0
    for _ in range(iterations):
        for _ in range(iterations):
            total += 1
    return str(total)


if __name__ == '__main__':
    app.run(debug=False)
