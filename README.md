
# EcoleDirecteApi

ecoledirecteapi est une librairie python permetant de communiquer simplement avec l'api ecole directe

## Exemple

```python
import ecoledirecteapi

client = ecoledirecteapi.Bot()
client.login("user", "pass")

print(client.evalAverage())
```

### Fonctions
```
    getApiUrl =>
    getApiVersion =>
    encodeString =>
    encodeBody =>
    getHeaders =>
    decodeB64 =>

    Bot.login
    Bot.isLogin
    Bot.getNotes
    Bot.evalAverage
    Bot.getHomeworks
    Bot.getSchoolLife
    Bot.getSchedules
    Bot.getMessages
```