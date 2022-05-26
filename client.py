
#usr/bin/python3


from logging import root

import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import socket 
from termcolor import colored 
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import kivy.graphics.instructions
from termcolor import colored


'''global s
s=socket.socket()
host='127.0.0.1'
port=1234'''
global host
host='127.0.0.1'
global port
port=1234




def show_popup():
    global popup 
    layout3=FloatLayout()
    layout=AnchorLayout(anchor_x='left',anchor_y='top')
    popupLabel=Label(text="Invalid Credential",font_size=30)
    layout2=AnchorLayout(anchor_x='left',anchor_y='bottom')
    button=Button(text="exit",pos=(10,10),size_hint=(.10,.10 ),height=10 ,width=10)
    layout2.add_widget(button)
    layout.add_widget(popupLabel)
    layout3.add_widget(layout2)
    layout3.add_widget(layout)
    popup=Popup(content=layout3)
    button.bind(on_press=popup.dismiss)
    popup.open()


class Login(Screen):
    login=ObjectProperty()
    #connect to server
    global credential
    global s 
    s=socket.socket()
    
    def screen_switch_two(self,*args):
       self.manager.current= 'Transaction'
    
    def screen_switch_three(self,*args):
       Bank().stop()
    

     # experience 
    def getCredential(self):
                s.connect((host,port))
            
                
                credential=self.ids.credential.text
                s.send(credential.encode())
                response=s.recv(1024).decode()
                if response=="success":
                    
                    print(colored("Hi YOU SUCCEED TO LOG IN... ",'green'))
                    Clock.schedule_once(self.screen_switch_two,3)
                    self.ids.status.color=(64/255,160/255,0/255,1)
                    self.ids.status.text='Hi,you have logged in succesffully...'
                    #self.manager.current='Transaction'
                    
                    
                    
                    
                    
                    
                    
                else:
                    print(colored("failure",'red'))
                    self.ids.status.text='Hi,Access is denied.. you\'ll be kicked out'
                    self.ids.status.color=(255/255,0/255,0/255,1)
                    Clock.schedule_once(self.screen_switch_three,3)
                    

                    

        
    #def credential(self):
    #       return credential

    def getsocket(self):
            return s

class Transaction(Screen):
    #first_screen = ObjectProperty()
    '''def starttimer(self):
        self.timer = Clock.schedule_once(self.screen_switch_two, 2)
    def screen_switch_two(self, dt):
        self.manager.current = 'second_screen'''

    def debit(self):
        s=Login().getsocket()
        
        s.send('I Want To Debit'.encode())
        data=s.recv(1024).decode()
        print(colored(data,'blue'))
                    
        self.manager.current='Debit'
                
            
     
    def credit(self):
        s=Login().getsocket()
        
        s.send('I Want To Credit'.encode())
        data=s.recv(1024).decode()
        
        print(colored(data,'blue'))
        self.manager.current='Credit'

    def showInvoice(self):
        s=Login().getsocket()
        s.send('Show Me Invoice'.encode())
        data=s.recv(1024).decode()
        print(colored(data,'blue'))
        self.manager.current='Invoice'
class Credit(Screen):
        #response=s.recv(1024).decode()
        #print(response)
        def screen_switch_two(self,*args):
                self.manager.current= 'Transaction'
    
         
        def crediter(self):
            s=Login().getsocket()
            creditAmount=self.ids.amountToCredit.text
            if creditAmount=="":
                print("nothing")
            
            else:
                s.send((creditAmount.encode()))
                response=s.recv(1024).decode()
                if response=="Inserted And Updated Successfully":
                        print(colored(response,'green'))
                        self.ids.hi.text="Operation is approved"
                        self.ids.hi.color=(64/255,160/255,0/255,1)
                        Clock.schedule_once(self.screen_switch_two,3)
                        
                elif response=="Inserted Successfully":
                        print(colored(response,'green'))
                        self.ids.hi.color=(64/255,160/255,0/255,1)
                        self.ids.hi.text="Operation is approved"
                        Clock.schedule_once(self.screen_switch_two,3)
                          
                else:
                        print(colored("Failure",'red'))
                        self.ids.hi.color=(255/255,0/255,0/255,1)
                        self.ids.hi.text="Operation is denied!"

                        Clock.schedule_once(self.screen_switch_two,3)  #if failure back to previous screen to start again connection with transaction(server)


class Debit(Screen):

        def screen_switch_two(self,*args):
                self.manager.current= 'Transaction'

        def debiter(self):
            s=Login().getsocket()
            DebitAmount=self.ids.amountToDebit.text
            
            s.send((DebitAmount.encode()))
            response=s.recv(1024).decode()
            if response=="Inserted And Updated Successfully":
                    print(colored(response,'green'))
                    self.ids.hello.color=(64/255,160/255,0/255,1)
                    self.ids.hello.text="Operation is approved"
                    Clock.schedule_once(self.screen_switch_two,3) 
                    
                    
            elif response=="Inserted":
                    print(colored(response,'green'))
                    self.ids.hello.color=(64/255,160/255,0/255,1)
                    self.ids.hello.text="Operation is approved"
                    Clock.schedule_once(self.screen_switch_two,3) 
                     
            else:
                    print(colored("Failure",'red'))
                    
                    self.ids.hello.color=(255/255,0/255,0/255,1)
                    self.ids.hello.text="Operation is denied!"
                    Clock.schedule_once(self.screen_switch_two,3) 
                    
class Invoice(Screen):
        def bill(self):
            s=Login().getsocket()
            s.send(('Show Me Invoice'.encode()))
            response=s.recv(1024).decode()
            print(colored(response,'green'))
            self.ids.bill.text=str(response)
        
            
            
            
            
            

class Bank(App):

    def build(self):
        return Builder.load_file('application.kivy')

if __name__ == '__main__':
    Bank().run()
    s.connect((host,port))

