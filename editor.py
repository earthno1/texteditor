'''pyinstaller Editor.py --add-data="./源码.ico;." -F -w -i 源码.ico'''
import os
import platform
import sys
from tkinter.filedialog import *
from tkinter.messagebox import *
# from tkinter.simpledialog import *
from tkinter import *

# import easygui

# from tkinter.ttk import *
if platform.system() == 'Windows':
    from tkinter.ttk import *


# 查找功能的窗口
def find_window(event=None):
    sw = Toplevel(main)
    sw.title('查找')
    sw.transient(main)
    sw.resizable(False, False)
    Label(sw, text="查找的文本:").grid(row=0, column=0)
    e = Entry(sw, width=50)
    e.grid(row=0, column=1)
    e.focus_set()
    Button(sw, text="全部查找", command=lambda: find_text(e.get(), ignore_case_value.get(), sw)).grid(row=0, column=2,
                                                                                                  sticky='e' + 'w',
                                                                                                  padx=2, pady=2)
    ignore_case_value = IntVar()
    Checkbutton(sw, text='不区分大小写', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)

    def on_closing():
        editor.tag_remove('match', '1.0', END)
        editor.tag_add('match', "1.0", END)
        editor.tag_config('match', foreground='black', background='white')
        sw.destroy()

    sw.protocol("WM_DELETE_WINDOW", on_closing)


# 光标框选查找的内容

def find_text(text, case, sw):
    editor.tag_remove('match', '1.0', END)
    num = 0
    if text:
        start_pos = '1.0'
        while True:
            start_pos = editor.search(text, start_pos, nocase=case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(text))
            editor.tag_add('match', start_pos, end_pos)
            start_pos = end_pos
            num = num + 1
        editor.tag_config('match', foreground='red', background='yellow')
        sw.title('找到了' + str(num) + '个“' + text + '”')


main = Tk()
path = None
main.title("文本编辑器 - 新的文本文件")
main.geometry("500x500")
zhidinv = False
line_number_bar = Text(main, width=4, padx=3, takefocus=0, border=0, background='khaki', state='disabled', wrap='none')
line_number_bar.pack(side='left', fill='y')


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


def redo(_=None):
    editor.event_generate("<<Redo>>")


def undo(_=None):
    editor.event_generate("<<Undo>>")


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
right_click_menu.add_command(label='撤销', command=undo)
right_click_menu.add_command(label='恢复', command=redo)


def right_click(event):
    right_click_menu.post(event.x_root, event.y_root)


def replace_window(_=None):
    rw = Toplevel(main)
    rw.title("替换")
    ff = Frame(rw)
    tf = Frame(rw)
    f = Entry(ff)
    t = Entry(tf)
    Label(ff, text="从文本：").pack(side=LEFT)
    Label(tf, text="替换为：").pack(side=LEFT)
    f.pack(side=LEFT)
    t.pack(side=LEFT)
    ff.pack()
    tf.pack()
    rf = Frame(rw)
    Button(master=rf, text="替换全部", command=lambda: replace_all(f, t)).pack(side=LEFT)
    Button(master=rf, text="替换", command=lambda: replace_one(f, t)).pack(side=LEFT)
    rf.pack()


def replace_one(f, t):
    from_str, to_str = f.get(), t.get()
    start_pos = editor.search(from_str, "1.0")
    if start_pos != "":
        end_pos = '{}+{}c'.format(start_pos, len(from_str))
        editor.replace(start_pos, end_pos, to_str)


def replace_all(f, t):
    from_str, to_str = f.get(), t.get()
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
edit.add_command(label='撤销 ctrl+z', command=undo)
edit.add_command(label='恢复 ctrl+y', command=redo)
edit.add_separator()
edit.add_command(label="全选 ctrl+a", command=choose_all)
edit.add_command(label="剪切 ctrl+x", command=cut)
edit.add_command(label="复制 ctrl+c", command=copy)
edit.add_command(label="粘贴 ctrl+v", command=paste)
edit.add_command(label="查找 ctrl+f", command=find_window)
edit.add_command(label="替换 ctrl+r", command=replace_window)

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
editor = Text(undo=True)
# op.pack(side = LEFT)
editor.pack(side=LEFT, expand=1)
# editor.bind('<KeyPress>',func=bigwmain)
main.config(menu=menu)
main.bind_all("<Control-s>", save_file)
main.bind_all("<Control-Shift_L><Key-S>", save_as_file)
main.bind_all("<Control-Shift_R><Key-S>", save_as_file)
main.bind_all("<Control-n>", new_file)
main.bind_all("<Control-o>", open_file)
main.bind_all("<Control-r>", replace_window)
main.bind_all("<Control-f>", find_window)
# timer = threading.Timer(1, fresher)
# timer.start()
bigwmain()
main.mainloop()
