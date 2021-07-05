import requests, json, sys,time,os,traceback
sys.path.append('class/')
from ApiRequest import ApiRequest
from decimal import *
from excepciones import Error
from logger import logger
from datetime import datetime
from dotenv import load_dotenv



def botTelegram(msg,minutes):
    Api=ApiRequest(SECTOKEN, LOG,   FICHEROLOG ,LOGLEVEL,URL) 
    respuesta=Api.EjecutaRequest(requests.get,[_TG+str(msg)],"")
    if minutes>10:
        if LOG:
            LOGGER.hazlog("botTelegram: Imposible comunicar con BOT "+ str(respuesta),1)
        raise Error(1,"botTelegram: botTelegram: Imposible comunicar con BOT  "+ str(respuesta))
    if isinstance(respuesta,int):
        if LOG:        
            LOGGER.hazlog("botTelegram- No es posible comunicar con bot de TG: "+ str(respuesta),1)
        time.sleep(60*minutes)
        return botTelegram(msg, minutes+1)
    else:
        return 200  

    

def requestSubgraph(Api,funcion,URL,payload,minutes):
    if minutes>10:
        if LOG:
            LOGGER.hazlog("requestSubgraph: Imposible conectar con subgraph ",1)
        raise Error(1,"requestSubgraph: Imposible conectar con subgraph")
    response=Api.EjecutaRequest(funcion,[URL],payload)
    if isinstance(response,int):
        if LOG:        
            LOGGER.hazlog("REGEN request: No es posible hacer obtener los datos  error: "+ str(response),1)
        time.sleep(60*minutes)
        return requestSubgraph (Api,requests.post,URL,payload,minutes+ 1)
    else:        
        return response.json() 

    

def QueryApiSubgraph(SC):
    noData=True
    dateProcess=datetime.now()       
    
    getcontext().prec = 7
    Api=ApiRequest(SECTOKEN, LOG,   FICHEROLOG ,LOGLEVEL,URL)
    #payload={"query":"\n  query oraclePrice {\n    \n       terra1jsxngqasf2zynj5kyh0tgq9mj3zksa5gk35j4k: WasmContractsContractAddressStore(\n      ContractAddress: \"terra1t6xe0txzywdg85n6k8c960cuwgh6l8esw6lau9\"\n            QueryMsg: \"{\\\"price\\\":{\\\"base_asset\\\":\\\"terra1jsxngqasf2zynj5kyh0tgq9mj3zksa5gk35j4k\\\",\\\"quote_asset\\\":\\\"uusd\\\"}}\"\n    )    {\n      Height\n      Result\n    }\n  }\n"}
    payload={"query":"\n  query oraclePrice {\n    \n       "+SC[0]+": WasmContractsContractAddressStore(\n      ContractAddress: \"terra1t6xe0txzywdg85n6k8c960cuwgh6l8esw6lau9\"\n            QueryMsg: \"{\\\"price\\\":{\\\"base_asset\\\":\\\""+SC[0]+"\\\",\\\"quote_asset\\\":\\\"uusd\\\"}}\"\n    )    {\n      Height\n      Result\n    }\n  }\n"}
    #Rewards Fondos paco
    res_json =requestSubgraph (Api,requests.post,URL,payload,1)
    print (res_json)
    print((res_json["data"][SC[0]]["Result"]))
    print(json.loads(str(res_json["data"][SC[0]]["Result"]))["rate"])
    valor=json.loads(str(res_json["data"][SC[0]]["Result"]))["rate"]
    if float(valor) <float(SC[1]):
        msg="El valor de " +str(SC[3])+ " esta por debajo del umbral "  +str(SC[1]) +" Precio actual " + str(valor)
        botTelegram(msg,1)
    if float(valor) >float(SC[2]):
        msg="El valor de " +str(SC[3])+ " esta por encima del umbral "  +str(SC[2]) +" Precio actual " + str(valor)
        botTelegram(msg,1)

    
    return 
    
# Load .ENV

try:
    load_dotenv()
    _TG=os.getenv("_TG")

    SECTOKEN=False if(os.getenv("SECTOKEN")=="False") else True
    LOG=False if(os.getenv("LOG")=="False") else True
    FICHEROLOG=os.getenv("FICHEROLOG")
    LOGLEVEL=int(os.getenv("LOGLEVEL"))
    DECIMALS=10**int(os.getenv("DECIMALS"))
    URL=os.getenv("URL")
    if LOG:
        LOGGER=logger(FICHEROLOG,LOGLEVEL)
        LOGGER.hazlog("Inicio programa",1)


    #SC=["terra1jsxngqasf2zynj5kyh0tgq9mj3zksa5gk35j4k",500,600,"mNetflix"]
    SC=os.getenv("SC").split(",")
   
    
    res=QueryApiSubgraph(SC)


    if res:
        raise Error(1,"Terra Oracle Proceso General: Se ha ejecutado con problemas")
      
except Exception as error:
    msg="Terra Oracle FALLO DEL PROCESO: "+str(error) +" "+str (traceback.format_exc()) 
    LOGGER.hazlog(msg,1)
    botTelegram(msg,1)



