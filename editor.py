'''pyinstaller Editor.py --add-data="./源码.ico;." -F -w -i 源码.ico'''
import os, sys
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
from tkinter import *

from tkinter.ttk import *

main = Tk()
path = None
main.title("文本编辑器 - 新的文本文件")
main.geometry("500x500")
zhidinv = False


def resource_path(relative_path):
    '''返回资源绝对路径。'''
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹temp
        # 并把路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


main.iconbitmap(resource_path(".\\源码.ico"))


def zhidin():
    global zhidinv
    if zhidinv:
        main.wm_attributes('-topmost', 0)
        zhidinv = False
    else:
        main.wm_attributes('-topmost', 1)
        zhidinv = True


def open_file(_=None):
    global path
    path = askopenfilename(title="文本编辑器 - 打开", filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
    if path and path != "":
        main.title("文本编辑器 - " + path)
        editor.delete("1.0", END)
        with open(path, "r", encoding="utf-8") as f:
            editor.insert(END, f.read())


def save_as_file(_=None):
    global path
    path = asksaveasfilename(title="文本编辑器 - 另存为", filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
    if path and path != "":
        main.title("文本编辑器 - " + path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", END))


def save_file(_=None):
    global path
    if path and path != "":
        with open(path, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", END))
    else:
        path = asksaveasfilename(title="文本编辑器 - 保存", filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if path and path != "":
            main.title("文本编辑器 - " + path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.get("1.0", END))


def new_file(_=None):
    global path
    path = None
    main.title("文本编辑器 - 新的文本文件")
    editor.delete("1.0", END)


def info():
    showinfo('关于', '此程序由 创新者.老王 与 渣渣_努力自闭ing 亲手打造')


def quitexit():
    sys.exit()
    quit()


def cut(event=None):
    editor.event_generate("<<Cut>>")


def copy(event=None):
    editor.event_generate("<<Copy>>")


def paste(event=None):
    editor.event_generate("<<Paste>>")


def choose_all(event=None):
    editor.event_generate("<<SelectAll>>")


# 右键菜单
right_click_menu = Menu(main, tearoff=0)
right_click_menu.add_command(label="全选", command=choose_all)
right_click_menu.add_command(label="剪切", command=cut)
right_click_menu.add_command(label="复制", command=copy)
right_click_menu.add_command(label="粘贴", command=paste)


def right_click(event):
    right_click_menu.post(event.x_root, event.y_root)


def replace_all(_=None):
    from_str = askstring("替换", "替换什么文本？")
    to_str = askstring("替换", "替换什么文本？")
    tmp = editor.get("1.0", END)
    editor.delete("1.0", END)
    editor.insert("1.0", tmp.replace(from_str, to_str))


main.bind_all("<Button-3>", right_click)

menu = Menu(main)
file = Menu(menu, tearoff=0)
file.add_command(label="新建 ctrl+n", command=new_file)
file.add_command(label="打开 ctrl+o", command=open_file)
file.add_command(label="保存 ctrl+s", command=save_file)
file.add_command(label="另存为 ctrl+shift+s", command=save_as_file)
edit = Menu(menu, tearoff=0)
edit.add_command(label="全选 ctrl+a", command=choose_all)
edit.add_command(label="剪切 ctrl+x", command=cut)
edit.add_command(label="复制 ctrl+c", command=copy)
edit.add_command(label="粘贴 ctrl+v", command=paste)
edit.add_command(label="替换 ctrl+r", command=replace_all)

menu.add_cascade(label="文件", menu=file)
menu.add_cascade(label="编辑", menu=edit)
menu.add_cascade(label="格式")
menu.add_cascade(label="查看")

mhelp = Menu(menu, tearoff=0)
mhelp.add_command(label="关于", command=info)
menu.add_cascade(label="帮助", menu=mhelp)
mcxz = Menu(menu, tearoff=0)
# zhidinbtn = mcxz.add_command(label = "置顶 x", command = zhidin)
mcxz.add_checkbutton(label="保持置顶", command=zhidin)
menu.add_cascade(label="特殊功能", menu=mcxz)
menu.add_command(label="退出", command=quitexit)


def bigwmain():
    main.update()
    editor["width"] = main.winfo_width()
    main.update()
    editor["height"] = main.winfo_height()
    main.update()

# op = Frame()
# newf = Button(master=op,text = "新建",command = new_file)
# openf = Button(master=op,text = "打开文件",command = open_file)
# saveasf = Button(master=op,text = "另存为",command = save_as_file)
# savef = Button(master=op,text = "保存",command = save_file)
# newf.pack()
# openf.pack()
# saveasf.pack()
# savef.pack()
editor = Text()
# op.pack(side = LEFT)
editor.pack(side=LEFT, expand=1)
# editor.bind('<KeyPress>',func=bigwmain)
main.config(menu=menu)
main.bind_all("<Control-s>", save_file)
main.bind_all("<Control-Shift_L><Key-S>", save_as_file)
main.bind_all("<Control-Shift_R><Key-S>", save_as_file)
main.bind_all("<Control-n>", new_file)
main.bind_all("<Control-o>", open_file)
main.bind_all("<Control-r>", replace_all)
# timer = threading.Timer(1, fresher)
# timer.start()
bigwmain()
main.mainloop()
