import requests
import base64

def getApiUrl():
    return "https://api.ecoledirecte.com/v3"

def getApiVersion():
    return "4.19.0"

def encodeString(string):
    return string.replace("%", "%25").replace("&", "%26").replace("+", "%2B").replace("+", "%2B").replace("\\", "\\\\\\").replace("\\\\", "\\\\\\\\")

def encodeBody(dictionnary, isRecursive = False):
    body = ""
    for key in dictionnary:
        if isRecursive:
            body += "\"" + key + "\":"
        else:
            body += key + "="
        
        if type(dictionnary[key]) is dict:
            body += "{" + encodeBody(dictionnary[key], True) + "}"
        else:
            body += "\"" + str(dictionnary[key]) + "\""
        body += ","

    return body[:-1]


def getHeaders(token = None):
    headers = {
        "authority": "api.ecoledirecte.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.ecoledirecte.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.ecoledirecte.com/",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    if token != None:
        headers["X-Token"] = token

    return headers

def decodeB64(string):
    return base64.b64decode(string)


class Bot:
    def __init__(self):
        self.token = None
        self.id = None

    def login(self, username, password):
        login = requests.post(f"{getApiUrl()}/login.awp?v={getApiVersion()}", data=encodeBody({
            "data": {
                "identifiant": username,
                "motdepasse": password
            }
        }), headers=getHeaders()).json()

        self.token = login["token"]
        self.id = login["data"]["accounts"][0]["id"]

    def isLogin(self):
        if self.token != None and self.id != None:
            return True

        return False

    def getNotes(self):
        if not self.isLogin():
            return None

        return requests.post(f"{getApiUrl()}/eleves/{self.id}/notes.awp?verbe=get&v={getApiVersion()}", data='data={"anneeScolaire": ""}', headers=getHeaders(self.token)).json()["data"]["notes"]

    def evalAverage(self):
        mnt = {}
        for x in self.getNotes():
            if x["libelleMatiere"] not in mnt:
                mnt[x["libelleMatiere"]] = {
                    "notes": [],
                    "coefs": []
                }
            
            mnt[x["libelleMatiere"]]["notes"].append(float(x["valeur"].replace(",", ".")) / float(x["noteSur"].replace(",", ".")) * 20)
            mnt[x["libelleMatiere"]]["coefs"].append(float(x["coef"].replace(",", ".")))

        for x in mnt:
            average = 0
            coef = 0
            for i in range(len(mnt[x]["notes"])):
                average += mnt[x]["notes"][i] * mnt[x]["coefs"][i]
                coef += mnt[x]["coefs"][i]

            mnt[x] = average / coef

        average = 0
        for x in [mnt[x] for x in mnt]:
            average += x
        average /= len(mnt)

        return average, mnt

    def getHomeworks(self, date):
        if not self.isLogin():
            return None

        return requests.post(f"{getApiUrl()}/Eleves/{self.id}/cahierdetexte/{date}.awp?verbe=get&v={getApiVersion()}", data='data={}', headers=getHeaders(self.token)).json()["data"]["mnt"]

    def getSchoolLife(self):
        if not self.isLogin():
            return None

        data = requests.post(f"{getApiUrl()}/Eleves/{self.id}/viescolaire.awp?verbe=get&v={getApiVersion()}", data='data={}', headers=getHeaders(self.token)).json()["data"]
        if "sanctionsEncouragements" not in data:
            data["sanctionsEncouragements"] = None

        return data["absencesRetards"], data["sanctionsEncouragements"]

    def getSchedules(self, startDate, endDate):
        if not self.isLogin():
            return None

        return requests.post(f"{getApiUrl()}/Eleves/{self.id}/emploidutemps.awp?verbe=get&v={getApiVersion()}", data=encodeBody({
            "data": {
                "dateDebut": startDate,
                "dateFin": endDate,
                "avecTrous": False
            }
        }), headers=getHeaders(self.token)).json()["data"]

    def getMessages(self, year):
        if not self.isLogin():
            return None

        return requests.post(f"{getApiUrl()}/Eleves/{self.id}/messages.awp?force=false&typeRecuperation=received&idClasseur=0&orderBy=date&order=desc&query=&onlyRead=&page=0&itemsPerPage=100&getAll=0&verbe=get&v={getApiVersion()}", data=encodeBody({
            "data": {
                "anneeMessages": year
            }
        }), headers=getHeaders(self.token)).json()["data"]