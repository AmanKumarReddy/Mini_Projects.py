import tkinter as tk

class DrawingPad:
    def __init__(self,root):
        self.root = root
        self.root.title("Python Drawing Pad")
        self.root.geometry("600x450")

        self.draw_color = "black"
        self.brush_size = 3
        self.old_x = None
        self.old_y = None

        self.toolbar = tk.Frame(self.root , bg="#f0f0f0", height=50)
        self.toolbar.pack(side = tk.TOP , fill=tk.X)

        tk.Label(self.toolbar , text="Size:" , bg="#f0f0f0" , font=("Helvtica", 10, "bold")).pack(side = tk.LEFT , padx = 10)
        self.size_slider = tk.Scale(self.toolbar , from_=1,to=20, orient=tk.HORIZONTAL , command=self.update_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side = tk.LEFT , padx=5)

        tk.Label(self.toolbar , text="Colours:", bg="#f0f0f0", font=("Helvetica" , 10 , "bold")).pack(side=tk.LEFT, padx=10)
        colors = ["violet" , "purple", "indigo" , "blue" , "green" , "yellow", "orange" , "red"]
        for color in colors:
            btn = tk.Button(self.toolbar, bg=color , width=3 , command = lambda c=color: self.change_color(c))
            btn.pack(side = tk.LEFT , padx=2,pady=5)

        self.eraser_btn = tk.Button(self.toolbar , text="Eraser", font =("Helvetica" , 9 , "bold"), command = self.use_eraser)
        self.eraser_btn.pack(side = tk.RIGHT , padx=10)


        self.clear_btn = tk.Button(self.toolbar, text = "Clear all" , font=("helvetica" , 9 , "bold"), bg="#ff4d4d", fg="white", command=self.clear_all)
        self.clear_btn.pack(side=tk.RIGHT, padx = 10)

        self.canvas = tk.Canvas(self.root, bg="white", cursor="pencil")
        self.canvas.pack(fill = tk.BOTH , expand = True)

        self.canvas.bind("<B1-Motion>" , self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)


    def paint(self,event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x , self.old_y , event.x , event.y , width = self.brush_size, fill=self.draw_color, capstyle=tk.ROUND , smooth=True)
        self.old_x = event.x
        self.old_y = event.y
    
    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def change_color(self , new_color):
        self.draw_color = new_color
        self.canvas.config(cursor = "pencil" )
    def use_eraser(self):
        self.draw_color = "white"
        self.canvas.config(cursor="pencil")

    def update_size(self , val):
        self.brush_size = int(val)

    def clear_all(self):
        self.canvas.delete("all")

if __name__ == '__main__':
    root = tk.Tk()
    app = DrawingPad(root)
    root.mainloop()