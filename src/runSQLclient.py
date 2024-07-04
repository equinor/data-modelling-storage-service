import json
from storage.repositories.plugin.sql import SQLClient
#NEED TO RUN THESE in terminal !
#docker-compose exec db_postgres psql -U postgres -d dmss"
#CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
study="""{
    "type": "models/signals_simple/Study",
    "cases": [
       {
          "name": "case1",
          "type": "models/signals_simple/Case",
          "description": "",
          "newAttribute": 32,
          "duration": 100,
          "timeStep": 0.1,
          "components": [
             {
                "type": "models/signals_simple/SinComp",
                "A": 10,
                "T": 10,
                "phase": 0.1
             },
             {
                "type": "models/signals_simple/SinComp",
                "A": 2,
                "T": 2,
                "phase": 0
             },
             {
                "type": "models/signals_simple/SinComp",
                "A": 20,
                "T": 20,
                "phase": 0.05
             }
          ],
          "signal": {
             "name": "signal",
             "type": "models/containers/EquallySpacedSignal",
             "value": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 1, 2 ,3, 4, 9],
             "xname": "time",
             "xunit": "s",
             "xdelta": 0.1,
             "xstart": 0,
             "xlabel": "Time",
             "label": " ",
             "legend": " ",
             "unit": "m"
          }
       }
    ]
}"""


client=SQLClient()
client.add_table('dmss://system/models/signals_simple/Study')
study=json.loads(study)
client.add(study)
"241ea1e7-c102-42cf-b51b-e3d555f09bbc"
print(client.get("241ea1e7-c102-42cf-b51b-e3d555f09bbc"))
print(client.delete("662fd344-f281-452a-8bdd-2c5a6731b22e"))
print(client.get("662fd344-f281-452a-8bdd-2c5a6731b22e"))
#print(client.get("d784efd3-575f-40c5-9711-8fe22bb64ab4"))
update_dict = {
    'A': 5,
    'T': 5,
    'phase':0.5,
    id:'76544'
}




#print(client.update("4ddc8812-1c9f-4e57-817b-d2767fbad47a",update_dict))

