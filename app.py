from flask import Flask, request
from fsm import machine
from utils import send_text_message
from fsm import machine

app = Flask(__name__)

VERIFY_TOKEN = "123123123"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    body = request.get_json()
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        try:
            e = { 'text': event['message']['text'],
                    'id': event['sender']['id'] }
            # print('msg', e)
            machine.advance(e)
            # send_text_message(e['id'], e['text'])
        except:
            pass
        return 'OKKKKK'

# @app.route('/show-fsm', methods=['GET'])
# def show_fsm():
#     machine.get_graph().draw('fsm.png', prog='dot', format='png')
#     return static_file('fsm.png', root='./', mimetype='image/png')

if __name__ == "__main__":
    app.run(debug = True, port = 5000)




