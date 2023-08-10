from flask import Flask, redirect, url_for, request, render_template, session, jsonify
from io import BytesIO
import requests, os, uuid, json
import array as arr
import numpy as np
from datetime import datetime, time,timedelta 
from datetime import timezone
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.cosmos import CosmosClient
import pytz

app = Flask(__name__)
@app.route('/', methods=['GET'])
def download():
    

       # in questa parte sto creando il nome della directory
    roomReq = request.args.get("Room")
    stanza=""
    if roomReq == "Seminterrato":
        stanza = "Stanza : Seminterrato"
    elif roomReq == "PrimoPiano":
        stanza = "Stanza : Primo Piano"  
    elif roomReq == "SecondoPiano":
        stanza = "Stanza : Secondo Piano"      
        
    # tutta questa paarte è per collegarsi a casmos DB
    endpoint= 'https://tesidblorenzo.documents.azure.com:443/' 
    key = '7S1tCyZQIAp6r0clF2cZ27bDCfV2uz4bB4XUmBHYvDcK5dF7T3IcEaKCpruLfXiqY9x6W8Mql83JACDbIGOJBA=='
    client = CosmosClient(endpoint, key)
    database_id = 'tesidblorenzo'
    container_id = 'tesidblorenzo'
    database = client.get_database_client(database_id)
    container = database.get_container_client(container_id)

    # visto che in cosmos DB vengono salvati in unix bisogna cambaire il tempo 
    rome_tz = pytz.timezone('Europe/Rome')

    #questa parte serve per dare un range temporale per prendere i dati da cosmos DB
    current_utc_time = datetime.utcnow()
    start_time = datetime.combine(current_utc_time.date(), time(8, 0))
    end_time = datetime.combine(current_utc_time.date(), time(18, 0))
    start_time_unix = int(start_time.timestamp())
    end_time_unix = int(end_time.timestamp())
    
    # quesato prende tutti i dati all'interno del range temporale selezionato prima
    query = f"SELECT * FROM c WHERE c._ts >= {start_time_unix} AND c._ts <= {end_time_unix}"

    #qui vengono messi i dati 
    items = list(container.query_items(query, enable_cross_partition_query=True))
    noise_10,noise_20,noise_30,noise_40,noise_50,noise_60=[],[],[],[],[],[]
    ore8_10,ore8_20,ore8_30,ore8_40,ore8_50,ore8_60=[],[],[],[],[],[]
    ore9_10,ore9_20,ore9_30,ore9_40,ore9_50,ore9_60=[],[],[],[],[],[]
    ore10_10,ore10_20,ore10_30,ore10_40,ore10_50,ore10_60=[],[],[],[],[],[]
    ore11_10,ore11_20,ore11_30,ore11_40,ore11_50,ore11_60=[],[],[],[],[],[]
    ore12_10,ore12_20,ore12_30,ore12_40,ore12_50,ore12_60=[],[],[],[],[],[]
    ore13_10,ore13_20,ore13_30,ore13_40,ore13_50,ore13_60=[],[],[],[],[],[]
    ore14_10,ore14_20,ore14_30,ore14_40,ore14_50,ore14_60=[],[],[],[],[],[]
    ore15_10,ore15_20,ore15_30,ore15_40,ore15_50,ore15_60=[],[],[],[],[],[]
    ore16_10,ore16_20,ore16_30,ore16_40,ore16_50,ore16_60=[],[],[],[],[],[]
    ore17_10,ore17_20,ore17_30,ore17_40,ore17_50,ore17_60=[],[],[],[],[],[]
    NoiseReturn = []
    orarioCartella = 0
    mediaNoiseFor=[]
    returnMediaNoise=[]
    mediaFinale = 0
    appNoise10=[]
    appNoise20=[]
    appNoise30=[]
    appNoise40=[]
    appNoise50=[]
    asseXorario=[]
    appMediafinale=0
    mediaFinaleReturn =[]


  
   
       
    NoiseReturn=[]
    returnMediaNoise=[]

    try:
            for item in items:
                print(len(items))
                asseXorario=[]
                room= item["Body"]["Room"]    #qua faccio il parser per l'rssi
                rssi= item["Body"]["RSSI"]
                orario = datetime.utcfromtimestamp(item["_ts"])
                rome_datetime = orario.replace(tzinfo=pytz.utc).astimezone(rome_tz)
                ora =rome_datetime.strftime("%H")
                ora = int(ora)
                minuti = rome_datetime.strftime("%M")  # anche questo probabilewmtne andrà cambiato
                minuti = int(minuti)
                if room == stanza:
                    noise = item["Body"]["Noise"] #qui c'e il rumore dello studio
                    try:
                        if ora == 8:
                            if minuti >=0 and minuti <10:
                                ore8_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore8_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore8_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore8_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore8_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore8_60.append(algoritmo(noise,rssi))
                        elif ora==9:
                            if minuti >=0 and minuti <10:
                                ore9_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore9_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore9_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore9_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore9_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore9_60.append(algoritmo(noise,rssi))
                        elif ora==10:
                            if minuti >=0 and minuti <10:
                                ore10_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore10_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore10_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore10_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore10_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore10_60.append(algoritmo(noise,rssi))
                        elif ora== 11:
                            if minuti >=0 and minuti <10:
                                ore11_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore11_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore11_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore11_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore11_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore11_60.append(algoritmo(noise,rssi))
                        elif ora==12:
                            if minuti >=0 and minuti <10:
                                ore12_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore12_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore12_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore12_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore12_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore12_60.append(algoritmo(noise,rssi))
                        elif ora==13:
                            if minuti >=0 and minuti <10:
                                ore13_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore13_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore13_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore13_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore13_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore13_60.append(algoritmo(noise,rssi))
                        elif ora ==14:
                            if minuti >=0 and minuti <10:
                                ore14_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore14_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore14_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore14_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore14_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore14_60.append(algoritmo(noise,rssi))
                        elif ora==15:
                            if minuti >=0 and minuti <10:
                                ore15_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore15_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore15_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore15_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore15_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore15_60.append(algoritmo(noise,rssi))
                        elif ora==16:
                            if minuti >=0 and minuti <10:
                                ore16_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore16_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore16_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore16_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore16_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore16_60.append(algoritmo(noise,rssi))
                        elif ora==17:
                            if minuti >=0 and minuti <10:
                                ore17_10.append(algoritmo(noise,rssi))
                            elif minuti >=10 and minuti<20:
                                ore17_20.append(algoritmo(noise,rssi))
                            elif minuti >=20 and minuti <30:
                                ore17_30.append(algoritmo(noise,rssi))
                            elif minuti >=30 and minuti<40:
                                ore17_40.append(algoritmo(noise,rssi))
                            elif minuti>=40 and minuti <50:
                                ore17_50.append(algoritmo(noise,rssi))
                            elif minuti>=50 and minuti <60:
                                ore17_60.append(algoritmo(noise,rssi))
                    except TypeError as e:
                            print(e)                  
            #calcolo il vettore finale
            if len(ore8_10) !=0:
                    NoiseReturn.append(np.mean(ore8_10))
            else:
                    NoiseReturn.append(0)
            if len(ore8_20) !=0:
                    NoiseReturn.append(np.mean(ore8_20))
            else:
                    NoiseReturn.append(0)
            if len(ore8_30) !=0:
                    NoiseReturn.append(np.mean(ore8_30))
            else:
                    NoiseReturn.append(0)
            if len(ore8_40) !=0:
                    NoiseReturn.append(np.mean(ore8_40))
            else:
                    NoiseReturn.append(0)
            if len(ore8_50) !=0:
                    NoiseReturn.append(np.mean(ore8_50))
            else:
                    NoiseReturn.append(0)
            if len(ore8_60) !=0:
                    NoiseReturn.append(np.mean(ore8_60))
            else:
                    NoiseReturn.append(0)
            if len(ore9_10) !=0:
                    NoiseReturn.append(np.mean(ore9_10))
            else:
                    NoiseReturn.append(0)
            if len(ore9_20) !=0:
                    NoiseReturn.append(np.mean(ore9_20))
            else:
                    NoiseReturn.append(0)
            if len(ore9_30) !=0:
                    NoiseReturn.append(np.mean(ore9_30))
            else:
                    NoiseReturn.append(0)
            if len(ore9_40) !=0:
                    NoiseReturn.append(np.mean(ore9_40))
            else:
                    NoiseReturn.append(0)
            if len(ore9_50) !=0:
                    NoiseReturn.append(np.mean(ore9_50))
            else:
                    NoiseReturn.append(0)
            if len(ore9_60) !=0:
                    NoiseReturn.append(np.mean(ore9_60))
            else:
                    NoiseReturn.append(0)
            if len(ore10_10) !=0:
                    NoiseReturn.append(np.mean(ore10_10))
            else:
                    NoiseReturn.append(0)
            if len(ore10_20) !=0:
                    NoiseReturn.append(np.mean(ore10_20))
            else:
                    NoiseReturn.append(0)
            if len(ore10_30) !=0:
                    NoiseReturn.append(np.mean(ore10_30))
            else:
                    NoiseReturn.append(0)
            if len(ore10_40) !=0:
                    NoiseReturn.append(np.mean(ore10_40))
            else:
                    NoiseReturn.append(0)
            if len(ore10_50) !=0:
                    NoiseReturn.append(np.mean(ore10_50))
            else:
                    NoiseReturn.append(0)
            if len(ore10_60) !=0:
                    NoiseReturn.append(np.mean(ore10_60))
            else:
                    NoiseReturn.append(0)
            if len(ore11_10) !=0:
                    NoiseReturn.append(np.mean(ore11_10))
            else:
                    NoiseReturn.append(0)
            if len(ore11_20) !=0:
                    NoiseReturn.append(np.mean(ore11_20))
            else:
                    NoiseReturn.append(0)
            if len(ore11_30) !=0:
                    NoiseReturn.append(np.mean(ore11_30))
            else:
                    NoiseReturn.append(0)
            if len(ore11_40) !=0:
                    NoiseReturn.append(np.mean(ore11_40))
            else:
                    NoiseReturn.append(0)
            if len(ore11_50) !=0:
                    NoiseReturn.append(np.mean(ore11_50))
            else:
                    NoiseReturn.append(0)
            if len(ore11_60) !=0:
                    NoiseReturn.append(np.mean(ore11_60))
            else:
                    NoiseReturn.append(0)
            if len(ore12_10) !=0:
                    NoiseReturn.append(np.mean(ore12_10))
            else:
                    NoiseReturn.append(0)
            if len(ore12_20) !=0:
                    NoiseReturn.append(np.mean(ore12_20))
            else:
                    NoiseReturn.append(0)
            if len(ore12_30) !=0:
                    NoiseReturn.append(np.mean(ore12_30))
            else:
                    NoiseReturn.append(0)
            if len(ore12_40) !=0:
                    NoiseReturn.append(np.mean(ore12_40))
            else:
                    NoiseReturn.append(0)
            if len(ore12_50) !=0:
                    NoiseReturn.append(np.mean(ore12_50))
            else:
                    NoiseReturn.append(0)
            if len(ore12_60) !=0:
                    NoiseReturn.append(np.mean(ore12_60))
            else:
                    NoiseReturn.append(0)
            if len(ore13_10) !=0:
                    NoiseReturn.append(np.mean(ore13_10))
            else:
                    NoiseReturn.append(0)
            if len(ore13_20) !=0:
                    NoiseReturn.append(np.mean(ore13_20))
            else:
                    NoiseReturn.append(0)
            if len(ore13_30) !=0:
                    NoiseReturn.append(np.mean(ore13_30))
            else:
                    NoiseReturn.append(0)
            if len(ore13_40) !=0:
                    NoiseReturn.append(np.mean(ore13_40))
            else:
                    NoiseReturn.append(0)
            if len(ore13_50) !=0:
                    NoiseReturn.append(np.mean(ore13_50))
            else:
                    NoiseReturn.append(0)
            if len(ore13_60) !=0:
                    NoiseReturn.append(np.mean(ore13_60))
            else:
                    NoiseReturn.append(0)
            if len(ore14_10) !=0:
                    NoiseReturn.append(np.mean(ore14_10))
            else:
                    NoiseReturn.append(0)
            if len(ore14_20) !=0:
                    NoiseReturn.append(np.mean(ore14_20))
            else:
                    NoiseReturn.append(0)
            if len(ore14_30) !=0:
                    NoiseReturn.append(np.mean(ore14_30))
            else:
                    NoiseReturn.append(0)
            if len(ore14_40) !=0:
                    NoiseReturn.append(np.mean(ore14_40))
            else:
                    NoiseReturn.append(0)
            if len(ore14_50) !=0:
                    NoiseReturn.append(np.mean(ore14_50))
            else:
                    NoiseReturn.append(0)
            if len(ore14_60) !=0:
                    NoiseReturn.append(np.mean(ore14_60))
            else:
                    NoiseReturn.append(0)
            if len(ore15_10) !=0:
                    NoiseReturn.append(np.mean(ore15_10))
            else:
                    NoiseReturn.append(0)
            if len(ore15_20) !=0:
                    NoiseReturn.append(np.mean(ore15_20))
            else:
                    NoiseReturn.append(0)
            if len(ore15_30) !=0:
                    NoiseReturn.append(np.mean(ore15_30))
            else:
                    NoiseReturn.append(0)
            if len(ore15_40) !=0:
                    NoiseReturn.append(np.mean(ore15_40))
            else:
                    NoiseReturn.append(0)
            if len(ore15_50) !=0:
                    NoiseReturn.append(np.mean(ore15_50))
            else:
                    NoiseReturn.append(0)
            if len(ore15_60) !=0:
                    NoiseReturn.append(np.mean(ore15_60))
            else:
                    NoiseReturn.append(0)
            if len(ore16_10) !=0:
                    NoiseReturn.append(np.mean(ore16_10))
            else:
                    NoiseReturn.append(0)
            if len(ore16_20) !=0:
                    NoiseReturn.append(np.mean(ore16_20))
            else:
                    NoiseReturn.append(0)
            if len(ore16_30) !=0:
                    NoiseReturn.append(np.mean(ore16_30))
            else:
                    NoiseReturn.append(0)
            if len(ore16_40) !=0:
                    NoiseReturn.append(np.mean(ore16_40))
            else:
                    NoiseReturn.append(0)
            if len(ore16_50) !=0:
                    NoiseReturn.append(np.mean(ore16_50))
            else:
                    NoiseReturn.append(0)
            if len(ore16_60) !=0:
                    NoiseReturn.append(np.mean(ore16_60))
            else:
                    NoiseReturn.append(0)
            if len(ore17_10) !=0:
                    NoiseReturn.append(np.mean(ore17_10))
            else:
                    NoiseReturn.append(0)
            if len(ore17_20) !=0:
                    NoiseReturn.append(np.mean(ore17_20))
            else:
                    NoiseReturn.append(0)
            if len(ore17_30) !=0:
                    NoiseReturn.append(np.mean(ore17_30))
            else:
                    NoiseReturn.append(0)
            if len(ore17_40) !=0:
                    NoiseReturn.append(np.mean(ore17_40))
            else:
                    NoiseReturn.append(0)
            if len(ore17_50) !=0:
                    NoiseReturn.append(np.mean(ore17_50))
            else:
                    NoiseReturn.append(0)
            if len(ore17_60) !=0:
                    NoiseReturn.append(np.mean(ore17_60))
            else:
                    NoiseReturn.append(0)
  
    except TypeError as e:
        print(e)
        return " non esiste la cartella"
    for k in range (8,18):
          asseXorario.append(k)
          asseXorario.append(k+1/6)
          asseXorario.append(k+2/6)
          asseXorario.append(k+3/6)
          asseXorario.append(k+4/6)
          asseXorario.append(k+5/6)
    
    filejsonReturn=({
        'Rumore': NoiseReturn,
        'X': asseXorario
    })
    print(len(NoiseReturn))
        
    prova =  jsonify(filejsonReturn)    #prova =  jsonify(NoiseReturn)
    return prova  # togliere questo e tuttto il commento per ripristinare il codice








    
@app.route('/istant', methods=['GET'])
def istant():
  
 roomReq = request.args.get("Room")
 stanza=""
 noise=""
 returnNoise=[]
 noiseReturn=0
 # questa è la logica per scegliere a quale stanza fare il parser
 if roomReq == "Seminterrato":
        stanza = "Stanza : Seminterrato"
 elif roomReq == "PrimoPiano":
        stanza = "Stanza : Primo Piano"  
 elif roomReq == "SecondoPiano":
        stanza = "Stanza : Secondo Piano"
    # tutta questa paarte è per collegarsi a casmos DB
 endpoint= 'https://tesidblorenzo.documents.azure.com:443/' 
 key = '7S1tCyZQIAp6r0clF2cZ27bDCfV2uz4bB4XUmBHYvDcK5dF7T3IcEaKCpruLfXiqY9x6W8Mql83JACDbIGOJBA=='
 client = CosmosClient(endpoint, key)
 database_id = 'tesidblorenzo'
 container_id = 'tesidblorenzo'
 database = client.get_database_client(database_id)
 container = database.get_container_client(container_id)
 current_time = datetime.now(timezone.utc) 
 time_stamp = current_time.timestamp()
 date_time = datetime.fromtimestamp(time_stamp)
 orarioH = date_time.strftime("%H")
 orarioM = date_time.strftime("%M")
 orarioHint = int(orarioH)
 orarioMint = int(orarioM)

 # visto che in cosmos DB vengono salvati in unix bisogna cambaire il tempo 
 rome_tz = pytz.timezone('Europe/Rome')

 #questa parte serve per dare un range temporale per prendere i dati da cosmos DB
 current_utc_time = datetime.utcnow()
 #prendo il minuto dopo
 start_time = datetime.combine(current_utc_time.date(), time(orarioHint, orarioMint-1))  #start_time = datetime.combine(current_utc_time.date(), time(8, 0))
 # prendo il minuto attuale come fine 
 end_time = datetime.combine(current_utc_time.date(), time(orarioHint, orarioMint))
 start_time_unix = int(start_time.timestamp())
 end_time_unix = int(end_time.timestamp())
    
 # quesato prende tutti i dati all'interno del range temporale selezionato prima, essendo quello istantaneo devo prendere la data della chiamata e come fine +1
 query = f"SELECT * FROM c WHERE c._ts >= {start_time_unix} AND c._ts <= {end_time_unix}"
 # qua ci sono tutti i dati di quel minuto
 items = list(container.query_items(query, enable_cross_partition_query=True))
 print(len(items))
 try:
      for item in items:
            print(len(items))
            room=item['Body']['Room']
            rssi=item['Body']['RSSI']
            if room == stanza:
                  if item["Body"]["Noise"] != float("-inf"):
                         noise = item["Body"]["Noise"]

                  returnNoise.append(algoritmo(noise,rssi))
 except:
       print("ciao")
 if len(returnNoise) !=0:     
        noiseReturn=np.mean(returnNoise)
 else:
        noiseReturn=0      
 print(returnNoise)
 return str(noiseReturn)            
        


 
 

        








def algoritmo(noiseAlgoritmo, rssiAlgoritmo):    #in assenza di ostacoli
    corpoFunzioneDistanza = (-70-rssiAlgoritmo)/40
    distanza = pow(10,corpoFunzioneDistanza)
    risultato= noiseAlgoritmo-10*np.log10(4*np.pi*distanza)
    return risultato
             

if __name__ == '_main_':
    app.run()    