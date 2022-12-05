import tkinter as tk
import socket
import pickle
import datetime
import threading
import logging  
#todo chatrooms and classes...blocking, select and stuff...disconnect...
def get_time():
    time=datetime.datetime.now()
    return time.strftime("%H:%M:%S")
def get_port():
    port=port_input.get("1.0",'end-1c')
    if ( port =="" ):
        port=3334
    return port

def start_server(port):
    global server_socket
    server_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server_socket.bind(('',int(port)))
        global online
        online = True
        server_socket.listen() 
        server_socket.setblocking(0)
        log_msg("Server started.")
    except Exception as e:
        log_msg("Error, could not bind socket. "+str(e))
        return

    t_chatt=threading.Thread(target=chatting_thread)
    t_list=threading.Thread(target=lambda:accepting_thread(server_socket))  
    t_chatt.start()
    t_list.start() 

def log_msg(msg):
    log_input.insert(tk.END, msg+"  |"+get_time()+"\n")

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
            try:
                msg=recv_msg(client)
            except Exception as e:
               # print(e)
               continue
        
            if(msg!=""):
                msg=sock_address[client][0]+" : "+msg
                log_msg("<<< " +msg)
                broadcast_msg(clients,msg)
                
    
def Quit():#
    online=False
    window.destroy()
def accepting_thread(server):
    while(online):
        try:
            (client_sock,client_adr)=server.accept()
        except Exception as e:
            #print(e)
            continue
        clients.append(client_sock)
        log_msg("Client connected: "+client_adr[0])
        sock_address[client_sock]=client_adr


online=False
server_ip="127.0.0.1"
server_socket=None 
clients=[]
sock_address={}
t_chatt=None
t_list=None
server_socket=None 

window=tk.Tk()
window.title("Chat server")
window.geometry('400x300')

port_label=tk.Label(text="Port:")
port_label.pack()

port_input=tk.Text(window,height=1,width=10)
port_input.insert(tk.END,"3334")
port_input.pack()

s_button_label=tk.Label(text="Press the button to start the server.")
#s_button_label.pack()

start_button=tk.Button(window,text="Run",command=lambda:start_server(get_port()))
start_button.pack()

#stop...

log_input=tk.Text(window,height=10,width=50)
log_input.pack()

window.protocol("WM_DELETE_WINDOW", Quit)
window.mainloop()


#?
if(t_chatt is not None):   
    t_chatt.join()
    t_list.join()