from flask import Flask, request, render_template
import json
import math


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/get_hamiltonian', methods = ['POST'])
def getHamiltonian():
    jsdata = request.form['javascript_data']
    data = json.loads(jsdata)

    qubits = []
    for x in range(data.qubitParameters.length):
        q = data.qubitParameters[x]
        match data.qubitType[x]:
            case "direct":
                qubits.append(q)
            case "coaxmon":
                qubits.append(math.Pi*q[0]**2/(math.Pi*q[2]**2 - math.Pi*q[1]**2))
            case "rectanglemon":
                qubits.append(q[0] * q[1] + q[2] * q[3])
            case _:
                return "error"


    freq = ["{}z{}".format(qubits[x],x) for x in range(qubits.length)]
    bais = []

    for x in range(data.weightMatrix.length):
        elmtX = data.weightMatrix[x]
        for y in range(elmtX.legth):
            elmt = elmtX[y]
            if (elmt != 0):
                 bais.append("{}z{}z{}".format(elmt, x+1,y+1))


    hString = "h ="
    for x in freq:
         hString += x
    for x in bais:
        hString += x

    return hString


#Json Data as follows
#QubitType
#QubitParameters
#WeightsMatrix


if __name__ == '__main__':
    app.run()
