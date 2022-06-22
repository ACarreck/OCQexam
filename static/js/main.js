window.addEventListener("load", ()=>{
    main = new Main()
})

class Main{
    //look this is a fever dream, as javascript always is
    //The callbacks make me queasy
    //but the page works nicely so
    constructor() {
        let html = document

        this.qubits = []
        this.qubitTypes = []
        this.connections = []

        let modal = html.getElementById("add-modal")
        let newQ = html.getElementById("add-button")

        let openSource = html.getElementById("source")
        let openMaths = html.getElementById("maths")

        openSource.onclick = () => window.open("https://github.com/ACarreck/OCQexam")
        openMaths.onclick = () => window.open('/download')

        let add = html.getElementById("add")
        let cancel = html.getElementById("cancel")

        cancel.onclick = () => modal.classList.remove("visible");
        newQ.onclick = () =>{
            modal.classList.add("visible");
            let selected = html.querySelector('input[name="radio"]:checked')
            selected.checked = false
            let dest = html.getElementById("connections-form")
            dest.innerHTML= ""

            let freqInputDirect = [html.getElementById("Dfreq")]
            let freqInputCoax = [html.getElementById("cr"),html.getElementById("ir"),html.getElementById("or")]
            let freqInputRect = [html.getElementById("l1"),html.getElementById("h1"),html.getElementById("l2"),html.getElementById("h2")]
            
            for (let x in freqInputDirect) freqInputDirect[x].disabled = true
            for (let x in freqInputCoax) freqInputCoax[x].disabled = true
            for (let x in freqInputRect) freqInputRect[x].disabled = true
        }

        let form = html.getElementById("add-form")

        let freqInputDirect = [html.getElementById("Dfreq")]
        let freqInputCoax = [html.getElementById("cr"),html.getElementById("ir"),html.getElementById("or")]
        let freqInputRect = [html.getElementById("l1"),html.getElementById("h1"),html.getElementById("l2"),html.getElementById("h2")]

        form.onchange = () => {
            let selected = html.querySelector('input[name="radio"]:checked').value
            switch (selected){
                case "direct":
                    for (let x in freqInputDirect) freqInputDirect[x].disabled = false
                    for (let x in freqInputCoax) freqInputCoax[x].disabled = true
                    for (let x in freqInputRect) freqInputRect[x].disabled = true
                    break

                case "coax":
                    for (let x in freqInputDirect) freqInputDirect[x].disabled = true
                    for (let x in freqInputCoax) freqInputCoax[x].disabled = false
                    for (let x in freqInputRect) freqInputRect[x].disabled = true
                    break

                case "rect":
                    for (let x in freqInputDirect) freqInputDirect[x].disabled = true
                    for (let x in freqInputCoax) freqInputCoax[x].disabled = true
                    for (let x in freqInputRect) freqInputRect[x].disabled = false
                    break
                default:
                    for (let x in freqInputDirect) freqInputDirect[x].disabled = true
                    for (let x in freqInputCoax) freqInputCoax[x].disabled = true
                    for (let x in freqInputRect) freqInputRect[x].disabled = true
                    break

            }
            let dest = html.getElementById("connections-form")
            let template = html.getElementById("connection").content.firstElementChild

            dest.innerHTML= ""

            let connections = []
            for (var x in this.qubits){
                let qnumber = x
                let label = "coupling to qubit" + qnumber + " "
                let qOption = template.cloneNode(true)
                let labelHtml = qOption.getElementsByClassName("con-label")[0]
                labelHtml.innerHTML = label
                dest.append(qOption)
            }


        }

        add.onclick = () => {
            let freqInputDirect = [html.getElementById("Dfreq").value]
            let freqInputCoax = [html.getElementById("cr").value,html.getElementById("ir").value,html.getElementById("or").value]
            let freqInputRect = [html.getElementById("l1").value,html.getElementById("h1").value,html.getElementById("l2").value,html.getElementById("h2").value]

            let form = html.getElementById("connections-form")
            let connectionInputs = Array.from(form.getElementsByClassName("con-number"))
            for(var x in connectionInputs){
                console.log(x)
                if (x !== this.qubits.length)  this.connections.push([connectionInputs[x].value,this.qubits.length,x])
            }


            modal.classList.remove("visible");
            let selected = html.querySelector('input[name="radio"]:checked').value
            switch (selected) {
                case "direct":
                    this.qubits.push(freqInputDirect)
                    this.qubitTypes.push("direct")
                    break

                case "coax":
                    this.qubits.push(freqInputCoax)
                    this.qubitTypes.push("coaxmon")
                    break

                case "rect":
                    this.qubits.push(freqInputRect)
                    this.qubitTypes.push("rectanglemon")
                    break
                case null:
                    break
                default:

                    break
            }

            let exportData = {"qubitType" : this.qubitTypes, "qubitParameters": this.qubits, "weights": this.connections}
            console.log(exportData)

            fetch('/get_hamiltonian', {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    method: 'POST',
                    body: JSON.stringify(exportData)
                }).then(function (response){

                if(response.ok) {
                    response.json()
                    .then(function(response) {
                        let outputStatus = html.getElementById("sucessOut")
                        let outputData = html.getElementById("dataOut")

                        if(response.response === "error"){
                            outputStatus.innerHTML = "Error in calc: "
                            outputData.innerHTML = response.msg
                            outputStatus.classList.add("error")
                            outputData.classList.add("error")
                        }else if (response.response === "success") {
                            outputData.innerHTML = response.msg
                        }else {
                            outputStatus.innerHTML = "Error in JSON: "
                            outputData.innerHTML = "Look I don't know how we got here but somehow we did"
                            outputStatus.classList.add("error")
                            outputData.classList.add("error")
                        }

                    })
                }
                else {
                    throw Error('Something went wrong');
                }
            })
            .catch(function(error) {
                console.log(error)
            })

        }
    }


}