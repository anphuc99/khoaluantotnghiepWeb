import json
from datetime import datetime, timedelta
import os

class Global:
    def getValue(key):
        try:
            file = open("Global/"+key+".json","r+")
            JsonData = file.read()       
            file.close()
            file_expire = open("Global/____expire_dates.json", "r+")  
            readExpire = file_expire.read()
            file_expire.close()
            if readExpire == "":
                readExpire = "{}"
            expire_date = json.loads(readExpire)
            RemoveKey = []
            for k,v in expire_date.items():
                if v < datetime.now().timestamp():
                    if os.path.exists("Global/"+k+".json"):
                        os.remove("Global/"+k+".json")
                    RemoveKey.append(k)
            
            for k in RemoveKey:                
                expire_date.pop(k, None)
            file_expire = open("Global/____expire_dates.json", "w+")  
            file_expire.write(json.dumps(expire_date))
            file_expire.close()
            return json.loads(JsonData)
        except Exception as e:
            raise Exception(e)
    
    def setValue(key, value, expire = 84600):
        try:
            file = open("Global/"+key+".json","w+")
            JsonData = json.dumps(value)
            file.write(JsonData)     
            file.close()
            if not os.path.exists("Global/____expire_dates.json"):
                open('Global/____expire_dates.json', 'w+').close()
            file_expire = open("Global/____expire_dates.json", "r+")
            readExpire = file_expire.read()
            file_expire.close()
            if readExpire == "":
                readExpire = "{}"
            expire_date = json.loads(readExpire)
            expire_date[key] = datetime.now().timestamp() + expire
            file_expire = open("Global/____expire_dates.json", "w+")
            file_expire.write(json.dumps(expire_date))
            file_expire.close()
        except Exception as e:
            raise Exception(e)