import json
from storage.repositories.plugin.sql.sql import SQLClient
from common.utils.package_import import import_package
from config import config
from authentication.models import User
#NEED TO RUN THESE in terminal !
#docker-compose exec db_postgres-1 psql -U postgres -d dmss"
#CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

user = User(
    **{
        "user_id": config.DMSS_ADMIN,
        "full_name": "Local Admin",
        "email": "admin@example.com",
    }
)
# import_package(
#      "/code/src/models5",
#      user,
#      data_source_name=config.CORE_DATA_SOURCE,
#      is_root=True,)

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
study2="""{
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
                "A": 100,
                "T": 20,
                "phase": 0.05
             }
          ],
          "signal": {
             "name": "signal",
             "type": "models/containers/EquallySpacedSignal",
             "value": [1, 2, 3, 4, 99, 6, 7, 1, 2, 3, 4, 5, 1, 2 ,3, 4, 9],
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



study2=json.loads(study2)
client=SQLClient()
client._verify_blueprint(study2)
print(client.add_table('dmss://system/models/signals_simple/Study'))
client.add(study2,'a2f4f64a-a71a-49fb-af2c-ff4ae96f5e49')
print(client.get("a1f4f64a-a71a-49fb-af2c-ff4ae96f5e49"))
#print(client.get("a1f4f64a-a71a-49fb-af2c-ff4ae96f5e49",all_data=False,levels=4))
#print(client.delete("a1f4f64a-a71a-49fb-af2c-ff4ae96f5e49"))
#client.add('a1f4f64a-a71a-49fb-af2c-ff4ae96f5e49',study2)
#print(client.get("a1f4f64a-a71a-49fb-af2c-ff4ae96f5e49"))
#print(client.get("d784efd3-575f-40c5-9711-8fe22bb64ab4"))
#print(client.update("a1f4f64a-a71a-49fb-af2c-ff4ae96f50",study2))

