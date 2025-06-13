import azure.functions as func
import logging
import json
from azure.identity import DefaultAzureCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="hello")
def hello_world(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Hello world-endepunkt ble kalt.')
    return func.HttpResponse("Hello, world!", status_code=200)

@app.route(route="get_token")
def get_token(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Henter Azure AD access_token for Microsoft Graph.')
    try:
        credential = DefaultAzureCredential()
        # Dette scope gir deg token til Microsoft Graph
        token = credential.get_token("https://graph.microsoft.com/.default").token

        return func.HttpResponse(
            json.dumps({"access_token": token}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Feil under token-henting: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
