# -*- coding:utf-8 -*-
#
import tkinter
import os

path = None
#Pycharm自己的from...import..，老王没瞎搞哈
from tkinter import END
from tkinter.filedialog import askopenfilename, asksaveasfilename

#老王找到的复制粘贴实现
def cut(event=None):
    t1.event_generate("<<Cut>>")
def copy(event=None):
    t1.event_generate("<<Copy>>")
def paste(event=None):
    t1.event_generate('<<Paste>>')

#窗口定义
window=tkinter.Tk()

#右键菜单
submenu=tkinter.Menu(window,tearoff=0)
submenu.add_command(label="剪切",command=cut)
submenu.add_command(label="复制",command=copy)
submenu.add_command(label="粘贴",command=paste)
def c(event):
    submenu.post(event.x_root,event.y_root)

window.bind("<Button-3>",c)


#窗体控件
t1=tkinter.Text()
t1.pack()

#老王补回来的菜单（垃圾的一批）
window.title("新的文本文件")

def open_file():
    global path
    path = askopenfilename(title="打开",filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
    if path and path!="":
        window.title(""+path)
        t1.delete("1.0",END)
        with open(path,"r",encoding="utf-8") as f:
            t1.insert(END,f.read())


def save_as_file():
    global path
    path = asksaveasfilename(title="另存为",filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
    if path and path != "":
        window.title(""+path)
        with open(path, "w",encoding="utf-8") as f:
            f.write(t1.get("1.0",END))
def save_file():
    global path
    if path and path != "":
        with open(path, "w",encoding="utf-8") as f:
            f.write(t1.get("1.0",END))
    elif path is None:
        path = asksaveasfilename(title="保存", filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if path and path != "":
            window.title("" + path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(t1.get("1.0", END))
def new_file():
    global path
    path = None
    window.title("新的文本文件")
    t1.delete("1.0",END)

menu = tkinter.Menu(window)
file = tkinter.Menu(menu, tearoff=0)
file.add_command(label="新建", command=new_file)
file.add_command(label="打开", command=open_file)
file.add_command(label="保存", command=save_file)
file.add_command(label="另存为", command=save_as_file)
menu.add_cascade(label = "文件", menu = file)
window.config(menu=menu)

window.mainloop()
