import tkinter as tk
import tkinter.simpledialog
import tkinter.scrolledtext
import customtkinter

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Black White")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=80)
        self.grid_rowconfigure(1, minsize=550)
        self.grid_rowconfigure(3, minsize=100)

        self.logo_label = customtkinter.CTkButton(self, text="Cobra Kai", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=(20,0),sticky="w")

        # Create a canvas to hold the chat frame
        self.chat_canvas = tk.Canvas(self, bg="white")
        self.chat_canvas.grid(row=1, column=1, rowspan=2, padx=(20,0), sticky="nsew")

        # Add a frame inside the canvas to hold the chat messages
        self.chat_frame = tk.Frame(self.chat_canvas, bg="white")
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        # Add a scrollbar for the canvas
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.chat_canvas.yview)
        self.scrollbar.grid(row=1, column=2, rowspan=2, sticky="ns")
        self.chat_canvas.config(yscrollcommand=self.scrollbar.set)

        self.input_field = customtkinter.CTkEntry(self, placeholder_text="Type your messages here......")
        self.input_field.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=3, padx=20)

        self.log = customtkinter.CTkFrame(self)
        self.log.grid(row=1,column=3,rowspan=2,padx=(20,20),sticky="nsew")

        self.button = customtkinter.CTkButton(self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text="Send",command=self.send)
        self.button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.input_field.bind("<Return>", self.send)

        self.appearance_mode_optionemenu.set("Dark")

        self.username = tkinter.simpledialog.askstring("Username", "Enter your username:")
        if self.username is None or self.username.strip() == "":
            self.destroy()

        # Configure the canvas scrolling
        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def send(self, event=None):
        message = self.input_field.get()
        length = len(message)
        message_modified = [message[i:i+153] for i in range(0, length, 153)]

        label = None 

        for i in range(len(message_modified)):
            if i == 0:
                lenz = len(message_modified[i])
                if message_modified[i][lenz-1] == " " or len(message_modified)<153:
                    label = customtkinter.CTkLabel(master=self.chat_frame, text=f"{self.username} -> {message_modified[i]}")
                elif len(message_modified) > 1:
                    label = customtkinter.CTkLabel(master=self.chat_frame, text=f"{self.username} -> {message_modified[i]}-")
            else:
                label = customtkinter.CTkLabel(master=self.chat_frame, text=f"{message_modified[i]}")

            if label:
                label.pack(padx=10, side=tk.TOP, anchor='w')

        self.input_field.delete(0, "end")
        self.chat_canvas.update_idletasks()  
        self.chat_canvas.yview_moveto(1.0)


    def divide_string(self, input_string, length):
        return [print(input_string[i:i+157]) for i in range(0, length, 157)]


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
