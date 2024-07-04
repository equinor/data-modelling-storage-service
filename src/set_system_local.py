from services.database import data_source_db
import json


system='''{
  "name": "system",
  "repositories": {
    "a": {
      "type": "mongo-db",
      "data_types": null,
      "host": "localhost",
      "port": 27017,
      "username": "maf",
      "password": "gAAAAABmfSGkg1ZX5lntm32Q4ejsyl9HS8sfVD7rBFKyha50P1dPejcbsK_Rm9mVB-edRHM0lh7Ohb159T-h8s4O77McMzR0aQ==",
      "database": "DMSS-core",
      "collection": "DMSS-core",
      "account_url": null,
      "container": null,
      "tls": false
    }
  },
  "_id": "system"
}'''
system=json.loads(system)
data_source_db.set("system",system)