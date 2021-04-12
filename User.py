import Pyro5.api
import os
import sys
import threading
from logs import Log

#funções de manipulação de arquivos proprios
def getFile(filename):
    try:
        f = open(filename,'r')
        return f.read()
    except FileNotFoundError:
        #arquivo nao existe
        return -1

def load_name_files(namedir):
    path = os.getcwd()
    path += '/' + namedir
    name_files = os.listdir(path)
    return name_files

#funcao que estabele contato entre nós (porta aberta pro pequeno mundo da nossa maquina)
@Pyro5.api.expose
class TorrentM(object):
    #ajuda a gravar arquivo
    def download(self,filename):
        filename_new = os.getcwd() + '/' + sys.argv[1] + '/'+ filename
        content_new_file = getFile(filename_new)
        return content_new_file


def load_balancing(myId, ids):
    
    if(len(ids) > 1):
        dif = -1
        id_file = -1
        for i in ids:
            #metrica pra simular o vizinho mais proximo
            cur_dif = abs(myId - i)
            if((dif == -1) or (cur_dif < dif)):
                dif = cur_dif
                id_file = i

        return id_file

    else:
        if(len(ids) == 1):
            return ids[0]
        else:
            return -1    
#se torna um peer no servidor de nomes


def insert_client_in_network(myId):
    #Talvez este não seja o melhor nome

    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(TorrentM)
    ns.register("Client:"+str(myId), uri)
    daemon.requestLoop()


def main():
   
    try:
        if( len(sys.argv) >= 2 ):
            log = Log("logUser.txt")
            namedir = sys.argv[1]
            client_ON = True
            try:
                network = Pyro5.api.Proxy("PYRONAME:Server")
                myId = network.connect(load_name_files(namedir))
            except(Pyro5.errors.CommunicationError):
                print("Server:OFF")
                myId = -1
        

            if(myId >= 0):  
                try:
                    t_network= threading.Thread(target=insert_client_in_network, args=(myId,))
                    t_network.daemon = True
                    t_network.start()
                except KeyboardInterrupt:
                    print(network.disconnect(myId))   

                print("Hello. Welcome a network!! Your id is ", myId)
            else:
                print("Sorry =( ")
                client_ON  = False
        else:
            print("Missing argument with your directory name: Ex.:python3 clientM myDirFiles")
            client_ON = False

        while(client_ON):
            
            op = int(input("Your options:\n[1] Show all files\n[2] Download\n[3] Update\n[4] Show file\n[5] Exit\n")) 
            os.system('clear')
            if(op == 1):
                print(network.show_filenames(myId))
            elif(op == 2):

                
                filename = str(input("What is the desired file name?\n"))
                ids = network.files_id(filename)
                idNeig = load_balancing(myId, ids)

                if(myId == idNeig):
                    print("Fail download")
                    print("You already have the file")
                else:
                    torrent = Pyro5.api.Proxy("PYRONAME:Client:"+str(idNeig))
                    content = torrent.download(filename)
                    if(content == -1):
                        print("Fail download")

                    else:


                        print("Sucess download")
                        filename_new = os.getcwd() + '/' + sys.argv[1] + '/'+ filename
                        new_file = open(filename_new,'w')
                        new_file.write(content)
                        new_file.close()       
                        network.update_files(myId,load_name_files(namedir))
                        log.new_log("FILE TRANSFER CLIENT:{} -> CLIENT:{} NAME FILE:{}".format(idNeig,myId,filename))
            
            
            elif(op == 3):
                    network.update_files(myId,load_name_files(namedir))
            elif(op == 4):
                idNeig  = int(input("What's the neighbor's ID?\n"))
                filename = str(input("What is the desired file name?\n"))
                if(idNeig == myId):
                    filename_new = os.getcwd() + '/' + sys.argv[1] + '/'+ filename
                    content = getFile(filename_new)
                    print("Name file {}\nCONTENT:".format(filename))
                    print(content)
                    log.new_log("SHOW FILE CLIENT:{} FILE:{}".format(myId,filename))
                else:
                    torrent = Pyro5.api.Proxy("PYRONAME:Client:"+str(idNeig))
                    content = torrent.download(filename)
                    if(content == -1):
                        print("None")
                    else:
                        print("Name file {}\nCONTENT:".format(filename))
                        print(content)
                        log.new_log("SHOW FILE DO CLIENT:{} FILE:{}".format(idNeig,filename))
            elif(op == 5):
                client_ON = False
                print(network.disconnect(myId))
            else:
                print("Option doesn't exists =(")
        #t_network.join()
    except(KeyboardInterrupt):
        print("\nBye!")
        print(network.disconnect(myId))
        
try:
    main()
except(Pyro5.errors.ConnectionClosedError):
    print("O administrador caiu! =( \n Desculpe o transtorne.")
   


