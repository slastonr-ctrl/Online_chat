from customtkinter import *
from socket import *
from threading import*


class MainWindow(CTk):
    def __init__ (self):
        super().__init__()
        self.geometry('400x300')
        self.title("козявка")

        self.menu_frame = CTkFrame(self, width = 30, height = 300)
        self.menu_frame.pack_propagate(0)
        self.menu_frame.place(x = 0, y = 0)

        self.is_show_menu = False
        self.speed_menu_anim = -5 

        self.btn = CTkButton(self, text = ">", width = 30, command = self.show_menu)
        self.btn.place( x = 0 , y = 0)

        self.chat_field = CTkScrollableFrame(self)
        self.chat_field.place(x = 0 , y = 0 )

        self.message = CTkEntry(self , placeholder_text= "Type your message here :", height = 40)
        self.message.place(x = 0 , y = 0 )

        self.chat_send = CTkButton(self, text = ">", width = 50 , height = 40 , command = self.send_message )
        self.chat_send.place(x = 0 , y = 0 )

        self.username = "Biba"
        try:
            self.socket = socket(AF_INET,SOCK_STREAM)
            self.socket.connect(("localhost", 8080))
            hello = f"{self.username}приєднався до чату!\n"
            self.socket.sendall(hello.encode())
            self.add_message(hello)
        except Exception as e :
            print(f"Упс, у вас сталася помилка - {e}")


        Thread(target = self.get_mes , daemon = True).start()




        self.adaptive_ui()

    def get_mes(self):
        while 1 : 
            try : 
                data = self.socket.recv(4096)
                if not data : 
                    break
                message = data.decode()
                self.add_message(message)
            except Exception as e : 
                print(f"error - {e}")
                break
        print("You were disconected")



    def send_message(self):
        text = self.message.get()
        if text : 
            full_message = f"{self.username} : {text}\n"
            try :
                self.socket.sendall(full_message.encode())
                self.add_message(full_message)
                self.message.delete(0 , END)
            except Exception as e : 
                print(f"error - {e}")






    def add_message(self,text):
        label = CTkLabel(self.chat_field,text=  text , anchor="w")
        label.pack(pady = 3 , fill = "x")




    def adaptive_ui(self):
        self.menu_frame.configure(height = self.winfo_height())

        self.chat_field.place(x = self.menu_frame.winfo_width())
        self.chat_field.configure(
            width = self.winfo_width() - self.menu_frame.winfo_width() - 20,
            height = self.winfo_height() - 40
        )

        self.chat_send.place(
            x = self.winfo_width() - self.chat_send.winfo_width(),
            y = self.winfo_height() - 40             
        )

        self.message.place(
            x = self.menu_frame.winfo_width(),
            y = self.chat_send.winfo_y()
        )

        self.message.configure(
            width = self.winfo_width() - self.menu_frame.winfo_width() - self.chat_send.winfo_width()

        )
        self.after(10, self.adaptive_ui)

    def show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_menu_anim *= -1
            self.btn.configure(text = ">")
            self.menu_anim()
        else:
            self.is_show_menu = True
            self.speed_menu_anim *= -1
            self.btn.configure(text = "<")
            self.menu_anim()
            self.label = CTkLabel(self.menu_frame, text = "Username")
            self.label.pack(pady = 20)
            self.entry = CTkEntry(self.menu_frame)
            self.entry.pack(pady = 10)



    def menu_anim(self):
        self.menu_frame.configure(width = self.menu_frame.winfo_width() + self.speed_menu_anim)
        if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.menu_anim)
        elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.menu_anim)
            if self.label and self.entry:
                self.label.destroy() 
                self.entry.destroy()  


win = MainWindow()
win.mainloop()