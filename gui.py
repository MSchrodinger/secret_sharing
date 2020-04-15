import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askretrycancel

p = [
    2,
    3,
    5,
    7,
    13,
    17,
    19,
    31,
    61,
    89,
    107,
    127,
    521,
    607,
    1279,
    2203,
    2281,
    3217,
    4253,
    4423,
    9689,
    9941,
    11213,
    19937,
    21701,
    23209,
    44497,
    86243,
    110503,
    132049,
    216091,
    756839,
    859433,
    1257787,
    1398269,
    2976221,
    3021377,
    6972593,
    13466917,
    20996011,
]
file_size = 0
path = ""
sheres = 0
thresh_hold = 0
file = ""


def chick_():
    global sheres, thresh_hold
    if sheres == 0:
        print(
            askretrycancel("askretrycancel", "you have not enterd number of shares!!")
        )
        return False

    elif thresh_hold == 0:
        print(
            askretrycancel(
                "askretrycancel", "you have not enterd number of thresh hold!!"
            )
        )
        return False
    else:

        return True


def chick_size():
    global file_size, path

    if path == "":
        print(askretrycancel("askretrycancel", "you have not select file yet!!"))
    elif file_size * 8 > p[-1]:
        print(askretrycancel("askretrycancel", "file size too big\nmax size: plapla"))
    elif file_size * 8 in p:
        if chick_():
            print(sheres)
    else:
        if chick_():
            for i in p:
                if i > file_size * 8:
                    file_size = i
                    break


def browse():
    global path, file_size
    path = askopenfilename()
    file_size = os.stat(path).st_size
    return path


def Encrypt_(win1):
    global sheres, thresh_hold, file
    win1.destroy()
    en = tk.Tk()
    f = tk.StringVar()

    widget1 = tk.Label(en, text="File path: ")
    widget1.grid(column=0, row=1)

    widget2 = tk.Label(en, textvariable=f)
    widget2.grid(column=1, row=1)

    browse_b = tk.Button(en, text="Browse", command=lambda: f.set(browse()))
    browse_b.grid(column=2, row=1)

    widget3 = tk.Label(en, text="Number of Shares: ")
    widget3.grid(column=0, row=2)

    widget4 = tk.Entry(en)
    widget4.grid(column=1, row=2)
    sheres = widget4.get()

    widget5 = tk.Label(en, text="Number of Thresh Hold: ")
    widget5.grid(column=0, row=3)

    widget6 = tk.Entry(en)
    widget6.grid(column=1, row=3)
    thresh_hold = widget6.get()

    Encrypt_b = tk.Button(en, text="Encrypt", command=lambda: chick_size())
    Encrypt_b.grid(column=0, row=4)

    cancel_b = tk.Button(en, text="Cancel", command=lambda: en.quit())
    cancel_b.grid(column=1, row=4)

    back_b = tk.Button(en, text="back", command=lambda: pick(en))
    back_b.grid(column=2, row=4)

    file = f.get()
    en.mainloop()


def Decrypt_(win1):
    win1.destroy()
    de = tk.Tk()
    file = tk.StringVar()

    widget1 = tk.Label(de, text="File path: ")
    widget1.grid(column=0, row=1)

    widget2 = tk.Label(de, textvariable=file)
    widget2.grid(column=1, row=1)

    browse_b = tk.Button(de, text="Browse", command=lambda: file.set(browse()))
    browse_b.grid(column=2, row=1)

    Encrypt_b = tk.Button(de, text="Decrypt", command=lambda: chick_size())
    Encrypt_b.grid(column=1, row=2)

    cancel_b = tk.Button(de, text="Cancel", command=lambda: de.quit())
    cancel_b.grid(column=2, row=2)
    de.mainloop()
    print(file)


def pick(wind=None):
    if wind == None:
        pass
    else:
        wind.destroy()
    pick = tk.Tk()

    b1 = tk.Button(pick, text="Encrypt", command=lambda: Encrypt_(pick))
    b1.grid(column=0, row=0)

    b2 = tk.Button(pick, text="Decrypt", command=lambda: Decrypt_(pick))
    b2.grid(column=2, row=0)

    b3 = tk.Button(pick, text="Cancel", command=lambda: pick.destroy())
    b3.grid(column=1, row=1)

    pick.mainloop()


pick()

print(thresh_hold)
