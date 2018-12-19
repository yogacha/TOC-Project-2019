import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = "EAAELUlHSLsIBAFRgzh0ZAppfxZCVjWb9aQpX1QaZCX1S6cN2nXnqUsTgoPcdzORP6cTJjReZCCfaxgcjQ2zZAwapM9LmY0SvZALjKruzdtvjANmnRLmENT7NRxTKY35iIixZCLZBJeB0KI0ZBAOJTbrYLatGZBivSqUiYEdbnOxcH2uwZDZD"


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
