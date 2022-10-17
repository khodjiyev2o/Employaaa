import http.client
import json
class Token:

    conn = http.client.HTTPSConnection("dev-p3f342pg.us.auth0.com")

    payload = "{\"client_id\":\"uykziHnUZ9KNhcwdfCYOZpPIhIoqJUOD\",\"client_secret\":\"7lUMJAiWlleWKTKTjp1zFA3ESJXHnTMyKdwyM24GItO4TpYnptuTkz14K-jWSo4b\",\"audience\":\"https://internship-api.com\",\"grant_type\":\"client_credentials\"}"

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    token=json.loads(data.decode("utf-8"))
    access_token = token.get("access_token") 




