from flask import Flask
from flask import request, render_template
import requests
import base64

app = Flask(__name__)

server_ip = "c8s2.op-framework.com" # Default Server (LimitlessRP Server 1)

url_players = "http://{}/players.json".format(server_ip)
url_info = "http://{}/info.json".format(server_ip)

@app.route('/', methods=['GET', 'POST'])
def main(server=None):
    if request.method == 'POST':
        server = request.form['servername']

        url_players = "http://{}/players.json".format(server)
        url_info = "http://{}/info.json".format(server)
        
    else:
        url_players = "http://{}/players.json".format(server_ip)
        url_info = "http://{}/info.json".format(server_ip)

    try:
        resp_players = requests.get(url_players)
        resp_players = sorted(resp_players.json(), key=lambda info: info['id'])

        resp_info = requests.get(url_info)

    except requests.exceptions.ConnectionError:
        return "There was a problem connecting to the FiveM server. The server might be currently offline."

    return render_template("index.html", info = resp_info.json(), players = resp_players, len = len(resp_players))

if __name__ == "__main__":
    app.run()
