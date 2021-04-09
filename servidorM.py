import Pyro5.api
from logs import Log

max_size = 50
clients = []
files = []
log = Log()

#Gerencia a geração de id's e verifica o limite de clientes na rede
def verrified_limit(file):
    idC = 0

    if( len(clients) < max_size ):

        for i in clients:
            if(i == -1):
                clients[idC] = idC
                files[idC] = file
                return idC
            idC += 1

        clients.append(idC)
        files.append(file)
        return idC
    else: 
        for i in clients:
            if(i == -1):
                clients[idC] = idC
                files[idC] = file
                return idC
            idC += 1

        return -1




@Pyro5.api.expose
class ServerP2P(object):    

    def connect(self, client_filenames):
        idC = verrified_limit(client_filenames)
        if( idC >= 0):
            
            log.new_log("CLIENT:{} CONNECT".format(idC))

            print("Success connection!!!\n Welcome to the network.")
            return idC
        else:
            log.new_log("FAIL CONNECT")
            
            print("Fail connection, sorry =( \n We are full.")
            return -1

    def disconnect(self, idC):
        log.new_log("CLIENT:{} DISCONNECT".format(idC))
        clients[idC] = -1
        files[idC] = None
        print("The client {} left!".format(idC))
        return "Server message: Hasta la vista! Client {}.".format(idC)
 

    def show_filenames(self, idC):
        all_files = ""
        for i in range( len(files) ):
            if(files[i] != None):
                for j in range(len(files[i])):
                    all_files += "Client ID:{} File Name:{}\n".format(i,files[i][j])
        log.new_log("CLIENT:{} LOOKED AT ALL FILES".format(idC))
        return all_files

    def update_files(self, idC, client_files):
        if(idC in clients):
            if(client_files == files[idC]):
                return("It was already up to date")
            else :
                #está desatualizado
                files[idC] = client_files
                log.new_log("CLIENT:{} UPDATE ALL FILES".format(idC))
                return("Updated!")


daemon = Pyro5.api.Daemon()
ns = Pyro5.api.locate_ns()
uri = daemon.register(ServerP2P)
ns.register("Server", uri)

print("Ready.")
daemon.requestLoop()
