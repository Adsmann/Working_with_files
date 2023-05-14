import threading
import uuid
import os
import time
from distutils.dir_util import copy_tree
from tkinter import *

path_start = r'C:\Users\MSI\Desktop\d'
tracker = 0

class File:

    def save(self):
        path = '{}'.format(txt.get())
        os.chdir(path)
        file_name = str(uuid.uuid4()) + '.txt'
        open(file_name, "w+")
        lbl.configure(text=file_name)
        os.chdir(path_start)

    def find_file(self):
        name = '{}'.format(txt.get())
        rootdir = 'f'
        if name in os.listdir(rootdir):
            lbl.configure(text=rootdir + "\\" + name)
        else:
            def listdirs(rootdir):
                for file in os.listdir(rootdir):
                    d = os.path.join(rootdir, file)
                    if os.path.isdir(d):
                        if name in os.listdir(d):
                            global a
                            a = d + "\\" + name
                        else:
                            listdirs(d)

            listdirs(rootdir)
            global a
            lbl.configure(text=a)
        os.chdir(path_start)

    def delete(self):
        name = '{}'.format(txt.get())
        rootdir = 'f'
        if name in os.listdir(rootdir):
            os.remove('f\\' + name)
            os.chdir(path_start)

        def listdirs(rootdir):
            for file in os.listdir(rootdir):
                d = os.path.join(rootdir, file)
                if os.path.isdir(d):
                    if name in os.listdir(d):
                        os.remove(d + '\\' + name)
                    else:
                        listdirs(d)

        listdirs(rootdir)
        os.chdir(path_start)

    def rename_file(self):
        b = ''
        c = ''
        name = '{}'.format(txt.get())
        for i in name:
            if i == " ":
                pass
            elif i == ",":
                b = c
                c = ''
            else:
                c += i
        rootdir = 'f'
        if b in os.listdir(rootdir):
            os.rename('f\\' + b, 'f\\' + c)

        def listdirs(rootdir):
            for file in os.listdir(rootdir):
                d = os.path.join(rootdir, file)
                if os.path.isdir(d):
                    if b in os.listdir(d):
                        os.rename(d + '\\' + b, d + '\\' + c)
                    else:
                        listdirs(d)

        listdirs(rootdir)
        os.chdir(path_start)

    def find_files(self):
        list_name = []
        name = '{}'.format(txt.get())
        c = ''
        for i in name:
            if i == " ":
                pass
            elif i == ",":
                list_name.append(c)
                c = ''
            else:
                c += i
        list_name.append(c)
        mass = []
        for name in list_name:
            rootdir = 'f'
            if name in os.listdir(rootdir):
                mass.append('f\\' + name)
                os.chdir(path_start)
            else:
                def listdirs(rootdir):
                    for file in os.listdir(rootdir):
                        d = os.path.join(rootdir, file)
                        if os.path.isdir(d):
                            if name in os.listdir(d):

                                mass.append(d + "\\" + name)
                            else:
                                listdirs(d)

                listdirs(rootdir)
        os.chdir(path_start)
        lbl.configure(text=mass)

    def file_list(self):
        rootdir = 'f'
        mass = []
        for i in os.listdir(rootdir):
            if i[-4:] == '.txt' and i not in mass:
                mass.append('f\\' + i)

        def listdirs(rootdir):
            for file in os.listdir(rootdir):
                d = os.path.join(rootdir, file)
                if os.path.isdir(d):
                    for i in os.listdir(d):
                        if i[-4:] == '.txt':
                            mass.append(d + "\\" + i)

                    listdirs(d)

        listdirs(rootdir)
        os.chdir(path_start)
        lbl.configure(text=mass)


def Backup():
    name = '{}'.format(txt.get())
    os.mkdir("C:\\Users\\MSI\\Desktop\\d\\b\\" + time.strftime('Year-%Y.%m.%d_') + time.strftime('hour-%H.%M.%S'))
    copy_tree("C:\\Users\\MSI\\Desktop\\d\\f",
              "C:\\Users\\MSI\\Desktop\\d\\b\\" + time.strftime('Year-%Y.%m.%d_') + time.strftime('hour-%H.%M.%S'))
    global T
    if name:
        T = threading.Timer(int(name) * 3600, Backup)
        T.start()
    os.chdir(path_start)


def Backup_load():
    list_dir = (os.listdir('b'))
    if "last_version" in list_dir:
        list_dir.remove("last_version")
    last_backup = max(list_dir)
    copy_tree("C:\\Users\\MSI\\Desktop\\d\\f",
              "C:\\Users\\MSI\\Desktop\\d\\b\\" + "last_version")
    copy_tree("C:\\Users\\MSI\\Desktop\\d\\b\\" + last_backup,
              "C:\\Users\\MSI\\Desktop\\d\\f")
    os.chdir(path_start)


def Backup_load_if_error():
    last_backup = max(os.listdir('b'))
    copy_tree("C:\\Users\\MSI\\Desktop\\d\\b\\" + last_backup,
              "C:\\Users\\MSI\\Desktop\\d\\f")
    os.chdir(path_start)


def Exit():
    T.cancel()
    exit(0)


T = threading.Timer(24 * 3600, Backup)
T.start()
pt = File()


def clicked():
    res = "Привет {}".format(txt.get())
    lbl.configure(text=res)


window = Tk()
window.title("Работа с файлами")
window.geometry('1000x700')
txt = Entry(window, width=100)
txt.grid(column=1, row=0)
btn = Button(window, text="Резервное копирование", command=Backup, width=30)
btn.grid(column=0, row=1)
btn = Button(window, text="Загрузить резервное копирование", command=Backup_load, width=30)
btn.grid(column=0, row=2)
btn = Button(window, text="Заргузка последней версии", command=Backup_load_if_error, width=30)
btn.grid(column=0, row=3)
btn = Button(window, text="Список файлов", command=pt.file_list, width=30)
btn.grid(column=0, row=4)
btn = Button(window, text="Удалить файл", command=pt.delete, width=30)
btn.grid(column=0, row=5)
btn = Button(window, text="Найти файл", command=pt.find_file, width=30)
btn.grid(column=0, row=6)
btn = Button(window, text="Переименовать файл", command=pt.rename_file, width=30)
btn.grid(column=0, row=7)
btn = Button(window, text="Сохранить файл", command=pt.save, width=30)
btn.grid(column=0, row=8)
btn = Button(window, text="Найти несколько файлов", command=pt.find_files, width=30)
btn.grid(column=0, row=9)
btn = Button(window, text="Выход", command=Exit, width=30)
btn.grid(column=0, row=10)
lbl = Label(window, text="", font=("Arial Bold", 10))
lbl.grid(column=1, row=4)
lbl2 = Label(window, text="", font=("Arial Bold", 10))
lbl2.grid(column=3, row=4)

window.mainloop()
T.cancel()
exit(0)
# r'C:\Users\MSI\Desktop\d\f\txt'
# pt.save('f\txt')
# pt.find_file('z.txt')
# pt.delete('z.txt')
# pt.rename_file("uwu.txt", '2.txt')
# pt.find_files(["z.txt","io.txt","2.txt"])
# pt.file_list()


# File.save(r'C:\Users\MSI\Desktop\d\f\txt')
# File.find_file('ad.txt')
# File.delete(r'f\txt\fd.txt')
# File.rename_file('1.txt', '2.txt')
