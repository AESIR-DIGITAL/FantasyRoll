#MIT License

#Copyright (c) 2023 Aesir Digital

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import random
import tkinter as tk
from tkinter import ttk
import os


class DiceRollerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        
        icon_path = os.path.abspath("icone\dice19.ico") #Image par: https://pixabay.com/fr/users/openclipart-vectors-30363
        self.iconbitmap(icon_path)

        self.title("FantasyRoll")
        self.geometry("600x400")
        self.resizable(width=False, height=False)

        

        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        
        bg_frame = tk.Frame(self.main_frame)
        bg_frame.pack(fill=tk.BOTH, expand=True)

        
        self.canvas = tk.Canvas(bg_frame, width=50, height=25)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        
        self.bg_image = tk.PhotoImage(file="image\d20.gif").subsample(5,5) #Image par: https://pixabay.com/fr/users/darkathena-5167878
        self.canvas.create_image(2, 3, image=self.bg_image, anchor="nw")

        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width = self.bg_image.width()
        image_height = self.bg_image.height()
        x = (canvas_width - image_width) // 2
        y = (canvas_height - image_height) // 2
        self.canvas.coords(self.bg_image, x, y)
        
        
        self.label = tk.Label(bg_frame, text="FantasyRoll", font=('Viking-Normal', 20, 'bold'), anchor="center")
        self.label.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        
        self.test_label = tk.Label(self, text="Copyright © 2023 \n Aesir Digital \n MIT License", font=('Arial', 7))
        self.test_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)

        
        self.dice_frame = tk.Frame(self.main_frame)
        self.dice_frame.pack(side=tk.LEFT, fill=tk.Y)


        
        self.history_frame = tk.Frame(self.main_frame)
        self.history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        
        self.dice_dict = {4: "d4", 6: "d6", 8: "d8", 10: "d10", 12: "d12", 20: "d20", 100: "d100"}
        for dice, label in self.dice_dict.items():
          button = tk.Button(self.dice_frame, text=label, command=lambda d=dice: self.roll_dice(d), 
                       borderwidth=5, relief=tk.RAISED, bd=3, 
                       highlightthickness=0, highlightbackground="#ffffff",
                       cursor='hand2',
          )
          button.pack(fill=tk.X, pady=1)


        
        self.expression_frame = tk.Frame(self.main_frame)
        self.expression_frame.pack(side=tk.TOP, fill=tk.X)

        
        entry_style = ttk.Style()
        entry_style.configure("Transparent.TEntry", background="#FFF", foreground="#AAA", borderwidth=0, alpha=0.5)


        
        self.expression_frame = tk.Frame(self)
        self.expression_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        
        self.expression_entry = tk.Entry(self.expression_frame, fg="black")
        self.expression_entry.insert(0, "ex: 2d6+1d12 or 1d20+1") 
        self.expression_entry.configure(fg="gray") 
        self.expression_entry.bind('<FocusIn>', self.on_entry_click) 
        self.expression_entry.bind('<FocusOut>', self.on_entry_leave) 
        self.expression_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        
        self.placeholder_text = "ex: 2d6+1d12 or 1d20+1"
    

        
        self.expression_button = tk.Button(self.expression_frame, text="Roll", command=self.roll_expression, 
                                   relief=tk.RAISED, bd=3, bg='#ffffff', fg='#000000', 
                                    
                                   highlightcolor='#ffffff', highlightthickness=0, 
                                   padx=2, pady=2, font=('Arial', 10), 
                                   borderwidth=2, width=3, height=1, 
                                   cursor='hand2', 
                                   )
        self.expression_button.pack(side=tk.LEFT)


        

        
        tk.Label(self.expression_frame, text=" ").pack(side=tk.LEFT)
        
        
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, pady=10)


        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_history,
                                relief=tk.RAISED, bd=3, bg='#ffffff', fg='#000000',
                                highlightcolor='#ffffff', highlightthickness=0, 
                                   padx=2, pady=2, font=('Arial', 12), 
                                   borderwidth=2, width=5, height=1, 
                                   cursor='hand2', 
                                   )
                                 
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)


        
        self.history_list = tk.Listbox(self.history_frame)
        self.history_list.pack(fill=tk.BOTH, expand=True)

        
    def roll_dice(self, dice):
        result = random.randint(1, dice)
        self.add_to_history(f"Rolling {self.dice_dict[dice]}: {result}")
        self.update_result(result)

    def roll_expression(self):
        expression = self.expression_entry.get().replace(" ", "")
        rolls = []
        total = 0
        for term in expression.split("+"):
            if "d" in term:
                num_dice, dice_size = term.split("d")
                num_dice = int(num_dice)
                dice_size = int(dice_size)
                rolls.append([random.randint(1, dice_size) for _ in range(num_dice)])
                total += sum(rolls[-1])
            else:
                total += int(term)
        self.add_to_history(f"Rolling {expression}: {total}")
        self.update_result(total)

    def add_to_history(self, message):
        self.history_list.insert(0, message)
    
    def update_result(self, result):
        self.result_str.set(str(result))

    def clear_history(self):
        self.history = []
        self.history_list.delete(0, tk.END) 

    def on_entry_click(self, event):
        """Supprime le texte fantôme lorsque l'Entry est cliquée."""
        if self.expression_entry.get() == "ex: 2d6+1d12 or 1d20+1":
            self.expression_entry.delete(0, "end") 

    def on_entry_leave(self, event):
        """Remet le texte fantôme s'il n'y a aucun texte dans l'Entry lorsqu'elle perd le focus."""
        if not self.expression_entry.get():
            self.expression_entry.insert(0, "ex: 2d6+1d12 or 1d20+1") 

    def on_entry_type(self, event):
    
     self.expression_entry.configure(fg=self.focused_text_color)

    def on_entry_click(self, event):
        if self.expression_entry.get() == self.placeholder_text:
            self.expression_entry.delete(0, tk.END) 
            self.expression_entry.config(fg="black") 

    def on_entry_leave(self, event):
        if self.expression_entry.get() == "":
            self.expression_entry.insert(0, self.placeholder_text) 
            self.expression_entry.config(fg="gray") 

            
if __name__ == "__main__":
    app = DiceRollerApp()
    app.mainloop()
