# Usual canary
def check_import():
    return True

# Config page generator
# It's kinda jank ngl
import json
def generate_config_file_structure():
    data = None
    with open("config.json", "r") as f:
        data = json.load(f)

    # First the head
    head = "<!DOCTYPE html>\n"
    head += "<html lang=\"en\"\n>"
    head += "<head>\n"
    head += "<meta charset=\"UTF-8\">\n"
    head += "<meta name=\"viewport\"\n"
    head += "content=\"width=device-width, initial-scale=1.0\">\n"
    head += f"<title>{ap_ssid}</title>\n"
    head += "<link rel=\"stylesheet\" href=\"styles.css\">\n"
    head += "</head>\n"

    # Now the hard part
    body = ""
    
    body += "<div class=\"innerContent\">\n"
    if ("debug" in data["general"] and data["general"]["debug"] == True) \
            and ("motd" in data["general"] and data["general"]["motd"] == "knock knock"):
                body += "<pre class=\".easteregg\">\n"
                body += "⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀<br>"
                body += " ⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣿⣷⣤⡀⠀⠀⠀⠀⠀<br>"
                body += " ⠀⠀⠀⠀⠀⠀⠀⣼⣿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠈⢻⣿⣿⡄⠀⠀⠀⠀<br>"
                body += " ⠀⠀⠀⠀⠀⠀⣸⣿⡏⠀⠀⠀⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄⠀⠀⠀<br>"
                body += " ⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⢰⣿⣿⣯⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⡄⠀<br>"
                body += " ⠀⣀⣤⣴⣶⣶⣿⡟⠀⠀⠀⢸⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀<br>"
                body += " ⢰⣿⡟⠋⠉⣹⣿⡇⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿⠀<br>"
                body += "⠀⢸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀<br>"
                body += "⠀⣸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⡇⠀⠀<br>"
                body += "⠀⣿⣿⠁⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀<br>"
                body += "⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀<br>"
                body += "⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀<br>"
                body += "⠀⢿⣿⡆⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀<br>"
                body += "⠀⠸⣿⣧⡀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀<br>"
                body += "⠀⠀⠛⢿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣰⣿⣿⣷⣶⣶⣶⣶⠶⠀⢠⣿⣿⠀⠀⠀<br>"
                body += "⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⣽⣿⡏⠁⠀⠀⢸⣿⡇⠀⠀⠀<br>"
                body += "⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⢹⣿⡆⠀⠀⠀⣸⣿⠇⠀⠀⠀<br>"
                body += "⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁⠀⠈⠻⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀<br>"
                body += "⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀<br>"
                body += "</pre>\n"
    
    body += "<h2>General:</h2>\n"
    for k, v in data["general"].items():
        body += f"<div><strong>{k}:</strong> {v}</div>\n"

    body += "<h2>Modes:</h2>\n"
    for k, v in data["modes"].items():
        body += f"<div><strong>Pin {k}:</strong> {v}</div>\n"

    for outer_key, inner_dict in data.items():
        if outer_key not in [ "general", "modes" ]:
            body += f"<h2>{outer_key}:</h2>\n"
            for inner_key, value in inner_dict.items():
                if len(inner_key) == 2:
                    body += f"<div><strong>Pin {inner_key}:</strong> {value}</div>\n"

    body += "</html>"

    return head + "\n" + body

# Set up wifi AP
import wifi
from ipaddress import ip_address

ap_ssid = "Bad64's Goblin"      # Obviously change this to whatever you see fit
ap_password = "NARPASSWORD"     # Ditto

wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
wifi.radio.set_ipv4_address_ap(
        ipv4=ip_address("10.0.0.1"),
        netmask=ip_address("255.255.255.0"),
        gateway=ip_address("10.0.0.1")
        )

# Now the server itself
import os
import socketpool

from adafruit_httpserver import Server, REQUEST_HANDLED_RESPONSE_SENT, Request, Response, FileResponse

pool = socketpool.SocketPool(wifi.radio)
localserver = Server(pool, "/webserver")

@localserver.route("/")
def home(request: Request):
    tempfile = generate_config_file_structure()
    return Response(request, tempfile, content_type="text/html")
