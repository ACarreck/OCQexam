from flask import Flask, request, render_template, send_file
#A lightweight webhosting app
from flask_assets import Bundle, Environment
#support for flask
import math
#🥧

app = Flask(__name__)

#oop this needed to show some OO
#There's OO in the javascript too
#this is unfortunately more of a script that flask uses,
# (flask has a factory system for class initation, it's very interesting

class DataProcessor:
    """ A Small Class that formats incoming data
        This data is formatted in a predictable way from a front end input system
        The class can then return a unicode and HTML formatted string for display in a web browser"""
    def __init__(self, data):
        """Json Data for the hamiltionain is formatted as follows
            QubitType
            QubitParameters
            weights
        you can call this function yourself in theory, just send an xml request.
        You're on your own thoough... It's recommended you use the front end to interact"""
        self.data = data

    def returnHamiltonian(self):
        """Returns a formatted Hamiltonian in a JSON response
         The response is as follows:
         {response:(error/success),msg:(error message/formatted hamiltonain)"""
        data = self.data
        qubits = []
        for x in range(len(data['qubitParameters'])):
            q = data['qubitParameters'][x]
            match data['qubitType'][x]:
                case "direct":
                    qubits.append(float(q[0]) / 2)
                case "coaxmon":
                    if ((math.pi * float(q[2]) - math.pi * float(q[1])) <= 0 or (math.pi * float(q[2]) - math.pi * float(q[0])) <= 0 ):
                        return {'resposnse': "error", 'msg': "Error, the outer radius must "
                                                             "be greater than the inner radius and center raduis for coaxmons"}
                    qubits.append(
                        (math.pi * float(q[0]) ** 2 / (math.pi * float(q[2]) ** 2 - math.pi * float(q[1]) ** 2) / 2))
                case "rectanglemon":
                    qubits.append((float(q[0]) * float(q[1]) + float(q[2]) * float(q[3])) / 2)
                case _:
                    return {'resposnse': "error", 'msg': "Error, wrong type for qubit"}

        freq = [" {}\u03C3<sub>z,{}</sub>".format(qubits[x], x) for x in range(len(qubits))]
        bais = []

        print(data['weights'])
        for w in data['weights']:
            if (float(w[0]) > 0):
                bais.append(" {}\u03C3<sub>x,{}</sub>\u03C3<sub>x,{}</sub>".format(w[0], w[1], w[2]))

        hString = "H ="
        for x in freq:
            hString += x + " +"
        for x in bais:
            hString += x + " +"

        print(hString)
        hString = hString[:-1]
        return {'response': "success", 'msg': hString}






@app.route('/get_hamiltonian', methods = ['GET','POST'])
def getHamiltonian():
    """
    you can actually just send these formatted requests to my server
    I'm not judging, maybe you need this for some reason
    :return: Json data about the input data, see DataProcessor.returnHamilton
    """
    data = request.get_json()
    processor = DataProcessor(data)
    return processor.returnHamiltonian()


def initAssets(app):
    """
    bundles the web assets so the front end looks nice and like... functions
    """
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


@app.route('/')
def hello_world():
    """
    The landing page
    """
    return render_template("main.html")


@app.route('/download')
def download():
    try:
        return send_file('static/pdf/mathsPortion.pdf', as_attachment=True)
    except Exception as e:
        return str(e)

@app.after_request
def gnu_terry_pratchett(resp):
    # "A man is not dead while his name is still spoken."
    # - Going Postal, Chapter 4
    # http://www.gnuterrypratchett.com/
    resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
    return resp



if __name__ == '__main__':
    #this app is too small to justify using factory properly
    initAssets(app)
    app.run(host='0.0.0.0')
