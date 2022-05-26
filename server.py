from concurrent.futures import thread
import socket

import sqlite3
from  _thread import *
from termcolor import colored
import traitement
import connection
ThreadCount=0
global ref
ref=''
s=socket.socket()
print("Socket successfully created")
port=1234
s.bind(('127.0.0.1',port))
print("socket binded to %s"%(port))
s.listen(5)

def client_thread(c):
    while True:
        #c,addr=s.accept()
        #print('Got connection from',addr)
        datafromclient=c.recv(1024).decode()
        
        if connection.verify_cred(connection.create_connection(),datafromclient)==True:
            
            c.send("success".encode())
            valid_credential=datafromclient
            conn=sqlite3.connect('../bank')
            cur=conn.cursor()
            getLogged="""select ref from credential where pass=?"""
            cur.execute(getLogged,(valid_credential,))
            key=cur.fetchall()[0][0]
            ref=str(key)
            #print(row) can uncommented

        else:
            c.send("failure".encode())
        '''data=c.recv(1024).decode() 
        print(data)
        data1=c.recv(1024).decode()
        print(data1)'''
        
        while True:
            data=c.recv(1024).decode() 
            
            if  data=='I Want To Debit':
                        #print(ref)
                        
                        print(colored(data,'blue'))
                        c.send('Enter The Amount To Debit'.encode())
                        response=c.recv(1024).decode()
                        print(colored(response,'blue'))
                        if traitement.debit(response,ref)=='Inserted And Updated Successfully':
                            c.send('Inserted And Updated Successfully'.encode())
                        elif traitement.debit(response,ref)=='Inserted Successfully':
                            c.send('Iserted Succefully'.encode())
                        else:
                            c.send('failure'.encode())
                            pass #treatment on database
            
                
            if  data=='I Want To Credit':
                        #print(ref)
                        print(colored(data,'blue'))
                        c.send('ENnter The Amount To Credit'.encode())
                        
                        response=c.recv(1024).decode()
                        
                        print(colored(response,'blue'))
                        if traitement.credit(response,ref)=='Inserted And Updated Successfully':
                            c.send('Inserted And Updated Successfully'.encode())
                            
                        else:
                            c.send('failure'.encode())
                            pass #treatment on database
            
            if  data=='Show Me Invoice':
                        print(colored(data,'blue'))
                        
                        c.send(traitement.invoice(ref).encode())
                    

while True:
    client,address=s.accept()
    print("connected to" + str(address[0])+" "+str(address[1]))
    start_new_thread(client_thread,(client,))
    ThreadCount+=1
    threadCount="ThreadCount="+str(ThreadCount)
    print(colored( threadCount,'blue'))