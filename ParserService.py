import socket
import sys
import signal
import threading
import json
import time

# CONSTANTES -----------------------------------------------------------
configfile = "config.txt"
sleepingtime = 30
UDP_IP = "localhost"
UDP_PORT = 10000
# ----------------------------------------------------------------------

# HANDLER DE SIGNAL ----------------------------------------------------
def handler(sig, frame):  # define the handler  
    print("Signal Number:", sig, " Frame: ", frame)  
    traceback.print_stack(frame)
# ----------------------------------------------------------------------	

# CLASE PARSER ---------------------------------------------------------
class Parser:
    def __init__(self,configfile):
        self.configfile = configfile
    
    def config_file(self):
        with open(self.configfile,'r') as f:
            readOut = f.readline()
        return readOut
    
    def read_csv(self,csv_path):
        with open(csv_path,'r') as f:
            header = next(f)
            line = f.readlines()
        return line
    
    def json_prep(self,lista):
        listaaux = []
        for fila in lista:
            sep = fila.split(",")
            dic = {}
            dic["id"] = int(sep[0])
            dic["value1"] = float(sep[2])
            dic["value2"] = float(sep[3])
            dic["name"] = sep[1]
            listaaux.append(dic)
        json_parse = json.dumps(listaaux)
        return json_parse
# ----------------------------------------------------------------------

# CREACION DE LA CLASE
parser = Parser(configfile)

# SIGNAL HANDLER
signal.signal(signal.SIGINT, handler)

# CREO EL SOCKET
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# FUNCION PRINCIPAL --------------------------------
def main():
    try:
        path = parser.config_file()                         #Busco el path de divisas
        path = path.rstrip("\n")                            #Le quito el \n al final del path
        while(True):                                        #Loop cada 30 segundos
            divlist = parser.read_csv(path)
            parseado = parser.json_prep(divlist)
            s.sendto(parseado.encode(), (UDP_IP, UDP_PORT))
            time.sleep(sleepingtime)
    except Exception as e:
        print("Error")
# --------------------------------------------------



# LLAMO A LA FUNCION PPAL --------------------------
main()

