import tkinter as tk

class Drawing:
    def __init__(self,root):
        self.root = root
        self.root.title("Drawing Pad")
        self.root.geometry("400x300")

        self.size = 3
        self.color = "black"
        self.old_x = None
        self.old_y = None

        self.frame = tk.Frame(self.root,bg="#cbdff4")
        self.frame.pack(side=tk.TOP , fill = tk.X)

        self.slide = tk.Label(self.frame , text="Size: ")
        self.slide.pack(side=tk.LEFT , padx=5)
        self.slider = tk.Scale(self.frame, from_=1, to=20, orient=tk.HORIZONTAL, command=self.update_size)
        self.slider.pack(side=tk.LEFT , padx=5)

        tk.Label(self.frame, text="Colours: ").pack(side=tk.LEFT , padx=10)
        colours = ["black",'purple',"violet","indigo","blue","green","yellow","orange","red"]
        for color in colours:
            btn = tk.Button(self.frame, width=6,height=6,bg=color,command = lambda c=color:self.update_c(c))
            btn.pack(side=tk.LEFT , padx=3)

        tk.Button(self.frame, text="Eraser",command=self.erase).pack(side=tk.RIGHT , padx=5)

        tk.Button(self.frame, text="Clear All",bg="red",command=self.clear ).pack(side=tk.RIGHT, padx=5)

        self.canvas = tk.Canvas(self.root , bg="white",cursor="pencil")
        self.canvas.pack(fill = tk.BOTH , expand = True)

        self.canvas.bind("<B1-Motion>",self.draw)
        self.canvas.bind("<ButtonRelease-1>",self.reset)

    def update_size(self,val):
        self.size = int(val)

    def update_c(self,val):
        self.color = val

    def erase(self):
        self.color = "white"

    def draw(self,event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x , self.old_y , event.x , event.y , width=self.size , fill=self.color , capstyle=tk.ROUND)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self,event):
        self.old_x = None
        self.old_y = None

    def clear(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = Drawing(root)
    root.mainloop()
