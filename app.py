from flask import Flask, request, render_template
from flask_assets import Bundle, Environment
import json
import math


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")

'''Json Data for the hamiltionain is formatted as follows
    QubitType
    QubitParameters
    weights
you can call this function yourself in theory, just send an xml request.
You're on your own tho... It's recommended you use the front end to interact'''


@app.route('/get_hamiltonian', methods = ['GET','POST'])
def getHamiltonian():
    data = request.get_json()
    print(data)
    qubits = []
    for x in range(len(data['qubitParameters'])):
        q = data['qubitParameters'][x]
        match data['qubitType'][x]:
            case "direct":
                qubits.append(float(q[0])/2)
            case "coaxmon":
                if((math.pi*float(q[2])**2 - math.pi*float(q[1])**2) <= 0):
                    return {'resposnse': "error", 'msg': "Error, the outer raduis must "
                                                         "be greater than the inner raduis for coaxmons"}
                qubits.append((math.pi*float(q[0])**2/(math.pi*float(q[2])**2 - math.pi*float(q[1])**2)/2))
            case "rectanglemon":
                qubits.append((float(q[0]) * float(q[1]) + float(q[2]) * float(q[3]))/2)
            case _:
                return {'resposnse': "error", 'msg': "Error, wrong type for qubit"}

    freq = [" {}\u03C3<sub>z,{}</sub>".format(qubits[x],x) for x in range(len(qubits))]
    bais = []

    print(data['weights'])
    for w in data['weights']:
        if(float(w[0]) > 0):
            bais.append(" {}\u03C3<sub>x,{}</sub>\u03C3<sub>x,{}</sub>".format(w[0], w[1],w[2]))


    hString = "H ="
    for x in freq:
         hString += x + " +"
    for x in bais:
        hString += x + " +"

    print(hString)
    hString = hString[:-1]
    return {'response': "success", 'msg':hString}


def initAssets(app):
    assets = Environment(app)

    main_js = Bundle(
        "js/main.js",
        output="gen/main.js"
    )

    assets.register("main_js", main_js)

    home_css = Bundle(
        "css/main.css",
        output="gen/home.css",
    )
    assets.register("home_css", home_css)

@app.after_request
def gnu_terry_pratchett(resp):
    # "A man is not dead while his name is still spoken."
    # - Going Postal, Chapter 4
    # http://www.gnuterrypratchett.com/
    resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
    return resp

if __name__ == '__main__':
    #this app is too small to justify using factory
    initAssets(app)
    app.run(debug=True)
