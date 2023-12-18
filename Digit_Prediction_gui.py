from tkinter import *
import win32gui
from PIL import ImageGrab, Image
import numpy as np
from tensorflow import keras
from tkinter import messagebox


np.random.seed(43)

def clear():
    c.delete("all")
    lbl.config(text="Draw here to Predict...")


def draw(event):
    x1,y1=event.x-8,event.y-8
    x2,y2=event.x+8,event.y+8
    c.create_oval(x1,y1,x2,y2,fill="black")

def predict(img):
    
    model=keras.models.load_model("My_model.h5")
    
    img=img.resize((28,28))
    img=img.convert('L')
    
    img=np.array(img)

    img=img/255.0
    img=np.where(img<1,1,0)
    
    img=img.reshape(1,28,28,1)

    result=model.predict(img)[0] 
    return np.argmax(result),max(result)
    

def img():
    
    h=c.winfo_id()
    w=win32gui.GetWindowRect(h)
    img=ImageGrab.grab(w)
    

    acc,num=predict(img)
    s=str(int(num*100))+"%"
    acc=str(acc)
    lbl.config(text=("Predicted : "+acc+', with '+s+' Accuracy'))
  
    
if __name__=="__main__":
    
    root=Tk()
    root.geometry("750x500")
    root.maxsize(780,500)
    root.minsize(780,500)
    root.title("Digit Prediction")
    root.configure(bg='lightgreen')


    f1=Frame(root,width=400,height=100,bg='lightgreen')
    f1.grid(row=4,column=4,padx=10)
    
    frame=Frame(root,width=400,height=400,bg="black",border=5)
    frame.grid(row=2,column=4,padx=20,pady=20)
    
    lbl=Label(root,text="Draw here to Predict...",font=("Times New Roman",25),fg='black',bg='lightgreen')
    lbl.grid(row=2,column=5)
    
    btn=Button(f1,text="Predict",command=img,width=10,height=3,fg="blue",border=5,activebackground='green')
    btn.grid(row=4,column=4,pady=5,padx=10)
    
    btn_2=Button(f1,text="Clear",command=clear,width=10,height=3,fg="red",border=5,activebackground='red')
    btn_2.grid(row=4,column=5,pady=5,padx=10)
    
    c=Canvas(frame,width=255,height=255,bg="white")
    c.pack()
    
    lbl2=Label(text="Draw digit between 0 and 9 ",bg='lightgreen',font=("Times New Roman",20),fg="blue")
    lbl2.grid(row=0,column=4,padx=10)
    
    root.bind("<B1-Motion>",draw)
    root.mainloop()