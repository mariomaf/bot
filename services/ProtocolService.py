import requests, json
import entity.protocol

protocolList = []


def getProtocols():
    # fetch all protocols
    r = requests.get('https://api.1inch.exchange/v3.0/56/protocols')
    data = json.loads(r.content)

    # create list of protocol Objects
    for protocol in data['protocols']:
        protocolList.append(entity.protocol.Protocol(protocol))
