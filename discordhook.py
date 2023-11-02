import requests
import json
from ocr import ocr_image

def sendLog():
    # Set webhook_url
    webhook_url = "https://discord.com/api/webhooks/1169668848543350844/X5O_km6L460Zd_J_j96FVinot064PuZ6p0Ya6w0TG1s0vcCW1WFmBDwvH5q7BmdBpJSp"

    logmessage = ocr_image("tribelog.png")
    message = {
        "content": f"{logmessage}"
    }

    #conert message to JSON string
    message_json = json.dumps(message)

    response = requests.post(webhook_url, data=message_json, headers={"Content-Type": "application/json"})

    if response.status_code == 204:
        print("message send succesfully")
    else:
        print("message failed to send")
        print(response.text)