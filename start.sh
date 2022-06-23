sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
sudo apt install python3.10-venv
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python3.10 app.py > log.text &
tail log.text -f