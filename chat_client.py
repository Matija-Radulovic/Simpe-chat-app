import urllib.request
import pygame as pg 
import random as rnd 
import math 
import socket 
import pickle
import threading 
import tkinter as tk 

import datetime

def ConnectPressed():
    server_address=server_address_var.get()
    port=server_port_var.get()
    try:
        client_socket.connect((server_address,int(port)))
        global connected
        connected=True
        Log("Successfully connected to "+ server_address+":"+port)
        OpenChat()
        listen_thread.start()
    except Exception as e:
        Log("Error connecting to "+ server_address+":"+port+" "+str(e))

def get_time():
    time=datetime.datetime.now()
    return time.strftime("%H:%M:%S")

def Log(msg): 
    log.insert("end-1c", msg+"  "+get_time()+"\n")

def Listener():
    while(connected):
        raw=client_socket.recv(1024)
        msg=raw.decode("utf-8")
        if msg:
            PrintMsg(msg+'\n')
            Log("Message received: "+msg)

def Myip():
    return urllib.request.urlopen('https://ident.me').read().decode('utf8')
def get_msg_txt():
    return input_send_msg.get("1.0",'end-1c')
def OpenChat():
    global window_chat,input_send_msg,input_recv_msg,send_button,connected
    window_chat=tk.Toplevel()
    window_chat.protocol("WM_DELETE_WINDOW", DisconnectPressed)
    
    input_recv_msg=tk.Text(window_chat,height=10,width=50)
    input_recv_msg.pack()

    
    input_send_msg=tk.Text(window_chat,height=1,width=30)
    input_send_msg.pack()

    send_button=tk.Button(window_chat,text="Send message",command=lambda:SendMsg(get_msg_txt()))
    send_button.pack()



def SendMsg(msg):
    try:
        client_socket.send(msg.encode("utf-8"))
        PrintMsg("(you)")
        Log("Message sent: "+msg)
    except Exception as e:
        Log("Error message not send "+str(e))

    pass#
def PrintMsg(msg):
    input_recv_msg.insert("end-1c", msg)
    pass#?
def DisconnectPressed():
    if not connected:   
        pass
    connected=False
    window_chat.destroy()
    listen_thread.join()
    Log("Disconnected")
    


client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address="127.0.0.1"
port=3334
connected=False
window_root=tk.Tk()
window_root.title("Chat client")
window_root.geometry('400x300')

input_address_label=tk.Label(text="Insert IP address")
input_address_label.pack()

server_address_var=tk.StringVar()
input_address=tk.Entry(window_root,textvariable=server_address_var)
input_address.insert(0,"127.0.0.1")
input_address.pack()

input_port_label=tk.Label(text="Insert port")
input_port_label.pack()

server_port_var=tk.StringVar()
input_port=tk.Entry(window_root,textvariable=server_port_var)
input_port.insert(0,"3334")
input_port.pack()


c_button_label=tk.Label(text="Press the button to connect.")
#c_button_label.pack()

connect_button=tk.Button(window_root,text="Connect",command=ConnectPressed)
connect_button.pack()


d_button_label=tk.Label(text="Press the button to disconnect.")
#d_button_label.pack()

disconnect_button=tk.Button(window_root,text="Disconnect",command=DisconnectPressed)
disconnect_button.pack()


log=tk.Text(window_root,height=10,width=50)
log.pack()


window_chat=None
input_send_msg=None 
send_button=None
input_recv_msg=None

listen_thread=threading.Thread(target=Listener)

window_root.mainloop()