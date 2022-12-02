import tkinter as tk
import socket
import pickle
import datetime
import threading
#todo chatrooms and classes...
def get_time():
    time=datetime.now()
    return time.strftime("%H:%M:%S")
def get_port():
    port=port_input.get("1.0",'end-1c')
    if ( port =="" ):
        port=3334
    return port
def start_server(ip,port):
    sock= socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.bind(ip,port)
        online=True
    except:
        log_msg("Error, could not bind socket.")

    if(online):
        t_chatt=threading.Thread(target=chatting_thread)
        t_list=threading.Thread(target=accepting_thread)  
        t_chatt.start()
        t_list.start() 
    pass
def log_msg(msg):
    log_input.insert("END", msg+"  |"+get_time())

def send_msg(client,msg):
    try:
        client.sendall(msg.encode("utf-8"))
        log_msg(">>> "+msg)
    except:
        log_msg("#Error, could not send message# : "+sock_address[client]+" : "+msg)
def broadcast_msg(clients,msg):
    for client in clients:
        send_msg(client,msg)

def recv_msg(client):
    data = client.recv(1024)
    return data.decode("utf-8")

def chatting_thread():
    while(online):
        for client in clients:
            msg=recv_msg(client)
            if(msg!=""):
                msg=sock_address[client]+" : "+msg
                log_msg("<<< "+msg)
                broadcast_msg(clients,msg)
                
    

def accepting_thread(server):
    while(online):
        (client_sock,client_adr)=server.accept()
        clients.append(client_sock)#lock?
        
        client_adr[client_sock]=client_adr


online=False
server_ip="127.0.0.1"
server_soket=None 
clients=[]
sock_address=None
t_chatt=None
t_list=None

window=tk.Tk()
window.title("Chat server")
window.geometry('400x300')

port_label=tk.Label(text="Port:")
port_label.pack()

port_input=tk.Text(window,height=1,width=10)
port_input.pack()

s_button_label=tk.Label(text="Press the button to start the server.")
s_button_label.pack()

start_button=tk.Button(window,text="Run",command=start_server)
start_button.pack()

#stop...

log_input=tk.Text(window,height=10,width=50)
log_input.pack()

window.mainloop()


#?
if(t_chatt is not None):   
    t_chatt.join()
    t_list.join()