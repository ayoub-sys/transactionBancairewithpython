#!/usr/bin/python3

from multiprocessing import Semaphore
from termcolor import colored
import sqlite3




my_obj=Semaphore(4)

#connection to database
def create_connection():
    conn=None
    try:

        conn=sqlite3.connect('../bank')


    except :
        print("failed to connect ")


    return conn

#verify login
global loggedName
def verify_cred(conn,credential):
    
    cur=conn.cursor()
    cur.execute("select pass,ref from credential")
    rows=cur.fetchall()
    access=0
    for row in rows:
      if credential==row[0]:
          access=1
          getLogged="""select client from credential where pass=?"""
          cur.execute(getLogged,(credential,))
          rows=cur.fetchall()
          loggedName='Client:'+rows[0][0]+'SUCCEED TO LOG IN'
          print(colored(loggedName,'green'))
          return True
          break 

    if access==0:
        failure="failed to login"
        print(failure)
        return False






#fetch all data from bien.txt
def fetchAccount():                                                 #fetch all accounts
    try:
        with open("account.txt","r") as f:
            
            s=f.readlines()
            
            f.close()
            return s
            
    except  : 
        print("error")

def fetchInvoice():                                        #fetch all invoices of clients
    my_obj.acquire()
    try:
        with open("invoice.txt","r") as f:
            
            s=f.readlines()
            f.close()
            return s

            
    except : 
        print("error")

    my_obj.release()


def selectAccount(ref):                                        #fetch th account of a specified client
    
    my_obj.acquire()
    table=fetchAccount()
    
    for line in table:
                if ref in line:
                    
                    toList=line.split()
                    print(toList)
                    return toList

                else:
                    
                    pass
    
   
    my_obj.release()


def updateAccount(ref,value,status):                        #make up to date to account.txt


    my_obj.acquire()          #locking section
    table=fetchAccount()
    #creating thread instance where count=3
    
    try:
        with open("account.txt","w") as f:
            for line in table:
                if ref in line:
                    str=''
                    toList=line.split()
                    #toList[0]='555'
                    toList[1]=value
                    toList[2]=status
                    
                    updatedline=' '.join(toList)
                    f.write(updatedline+'\n')
                else:
                    
                    f.write(line)
    
    except :
        print("error")
    my_obj.release()


def insertTransaction(ref,trans,money,result,status):         #insert transaction in file transaction.txt
    
    my_obj.acquire()
    try:
        with open("transaction.txt","a") as f:
            
            newtransaction=ref+' '+trans+' '+money+' '+result+' '+status+'\n'
            f.write(newtransaction)
            f.close()
            
            
    except : 
        print("error")
    my_obj.release()





def selectTransaction(ref,trans,result,status):           # return amount of money that client should pay to bank made by an account
    
    my_obj.acquire()    #locking
    try:
        with open("transaction.txt","r") as f:
            s=f.readlines()
            som=0
            for line in s:
                linetoList=line.split()
                if linetoList[0]==ref and linetoList[1]==trans and linetoList[3]==result and linetoList[4]==status:
                    som+=int(linetoList[2])*0.02
                    somme=str(som)
                
            f.close()
            print(somme)
            return somme

    except :
        print("error")
        my_obj.release()  #unlocking





def selectInvoice(ref):                                        #fetch th account of a specified client
    table=fetchInvoice()
   

    for line in table:
        if ref in line:
            toList=line.split()
            print(toList[1])
            return toList[1]
        else:
            print("no foundedd")
        
    
    



def updateInvoice(ref,som):             # make up to date the file 'invoice.txt'
    
    my_obj.acquire()
    table=fetchInvoice()
    try:
        with open("invoice.txt","w") as f:
            for line in table:
                if ref in line:

                    str=''
                    toList=line.split()
                    toList[0]=ref
                    toList[1]=som
                    
                    
                    updatedline=' '.join(toList)
                    f.write(updatedline+'\n')
                else:
                    
                    f.write(line)
    
    except :
        print("error")
    my_obj.release()






def credit(money,ref):
        result=''
        '''sqlite_insert_query=""" insert into  transaction (ref,transaction,values,result,status) values (?,?,?,?,?)"""
        trans="credit"
        res="success"
        ref="ref" 

        cur=conn.cursor()
        verif="""select value,status from account where ref=?"""
        cur.execute(verif,(credential,))'''
        trans="credit"
        cur=selectAccount(ref)
        value=cur[1]
        status=cur[2]
        if status=='positif':            #status always positif
            
            a=int(value)+int(money)                #resultat always success
            value=str(a)
            resultat='success'
            print(colored(resultat,'magenta')) 
            print(colored(status,'magenta')) 
            print(colored(value,'magenta'))
            #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
            insertTransaction(ref,trans,money,resultat,status)                #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
            updateAccount(ref,value,status)
            result='Inserted And Updated Successfully'
            return result
            

        if status=='negatif':          #resultat always success
            if (int(money) >= int(value)):
                a=int(money)-int(value)
                resultat='success'
                status='positif'
                value=str(a)
                print(colored(resultat,'magenta')) 
                print(colored(status,'magenta')) 
                print(colored(value,'magenta'))
                insertTransaction(ref,trans,money,resultat,status)                #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
                updateAccount(ref,value,status)
                result='Inserted And Updated Successfully'
                return result

            else:                      #status negatif
                a=int(value)-int(money)
                status='negatif' 
                resultat='success'  
                value=str(a)

                print(colored(resultat,'magenta')) 
                print(colored(status,'magenta')) 
                print(colored(value,'magenta'))
                insertTransaction(ref,trans,money,resultat,status)                #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
                updateAccount(ref,value,status)
                result='Inserted And Updated Successfully'
                return result


#operation on debit
def debit(money,ref):
        '''cur=conn.cursor()
        verif="""select value,status,maxdebit from account where ref=?"""
        cur.execute(verif,(credential,))'''
        result=''
        trans='debit'
        cur=selectAccount(ref)
        
        value=cur[1]
        status=cur[2]
        maxdebit=cur[3]
        
        
        if status=='positif':                #status always positif
            
            if (int(money) <= int(value)) :
                    resultat="success"
                    print(colored(resultat,'magenta'))
                    print(colored(status,'magenta'))
                    insertTransaction(ref,trans,money,resultat,status)
                    a=int(value)-int(money)
                    value=str(a)
                    print(colored(value,'magenta'))
                    updateAccount(ref,value,status)
                    result='Inserted And Updated Successfully' 
                    return result 
            
            
            else:
                if(int(money)-int(value)<=int(maxdebit)):
                    
                    a=int(money)-int(value)
                    value=str(a)  
                    resultat="success"
                    status="negatif" 
                    print(colored(resultat,'magenta')) 
                    print(colored(status,'magenta')) 
                    print(colored(value,'magenta'))
                    insertTransaction(ref,trans,money,resultat,status)                #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
                    updateAccount(ref,value,status)
                    result='Inserted And Updated Successfully'
                    return result
                
                else:
                     
                    resultat="fail"
                    status="positif" 
                    print(colored(resultat,'magenta')) 
                    insertTransaction(ref,trans,money,resultat,status)                #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
                    result='Inserted Successfully'
                    return result
           



        if status=='negatif':

            if (int(money)+int(value) <= int(maxdebit)) :
                    #print(money)
                    a=int(money)+int(value)
                    value=str(a)
                    resultat="success"
                    print(colored(resultat,'magenta')) 
                    print(colored(status,'magenta')) 
                    print(colored(value,'magenta'))
                    insertTransaction(ref,trans,money,resultat,status)                #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
                    updateAccount(ref,value,status)
                    result='Inserted And Updated Successfully'
                    return result 

            else:
                    #print(money)
                    resultat="fail"
                    status='negatif'
                    print(colored(resultat,'magenta')) 
                    insertTransaction(ref,trans,money,resultat,status)                #cur.execute(sqlite_insert_query,(ref,trans,money,res,status))
                    updateAccount(ref,value,status) 
                    
                    result='Inserted Successfully'
                    return result

#operation invoice 
def invoice(ref):
        
            trans="debit"
            result="success"
            status="negatif"
            
            somToPay=selectTransaction(ref,trans,result,status)
            #table invoice
            updateInvoice(ref,somToPay)
            data=selectInvoice(ref)
            #b=str(data)
            print(data)
            return data
            

            
#if __name__ == '__main__':
 #  updateInvoice('1000','')

                
