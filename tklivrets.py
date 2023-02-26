from tkinter import ttk, filedialog, Tk, StringVar, IntVar, messagebox
from livrets import convert, parseArgs
import sys

root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()

# button_style = ttk.Style().configure("TButton", relief="raised", padding=3)

path_in, path_out, border, sheets = parseArgs(sys.argv[1:])
vborder = StringVar()
vborder.set(border)
vsheets = IntVar()
vsheets.set(sheets)

def setInput():
    global path_in
    path_in = filedialog.askopenfilename(title="Fichier à convertir")
    label_in.configure(text=path_in)


def setOutput():
    global path_out
    path_out = filedialog.asksaveasfilename(title="Fichier dans lequel écrire le résultat")
    label_out.configure(text=path_out)


def progressCallback(value, max):
    print(f" => {value} / {max}")
    progress.configure(maximum=max, value=value)
    progress.update_idletasks()


def launch():
    if path_in is None or path_out is None:
        messagebox.showerror(title="Erreur", message="Les noms de fichiers en entrée et sortie sont obligatoires")
        return
    border = vborder.get()[0]
    sheets = vsheets.get()
    print(f"run {path_in} {path_out} {border} {sheets}")
    convert(path_in, path_out, border, sheets, progressCallback)
    progress.configure(maximum=100, value=100)
    messagebox.showinfo(message="Conversion terminée")


button_in  = ttk.Button(frame, text="Fichier d'entrée", command=setInput)
button_in.grid(column=0, row=0)
label_in = ttk.Label(frame, text=path_in)
label_in.grid(column=1, row=0)

button_out = ttk.Button(frame, text="Fichier de sortie", command=setOutput)
button_out.grid(column=0, row=1)
label_out = ttk.Label(frame, text=path_out)
label_out.grid(column=1, row=1)

label_border = ttk.Label(frame, text="verso sur bord")
label_border.grid(column=0, row=2)
combo_border = ttk.Combobox(frame, values = ['long' , 'court'], textvariable=vborder)
combo_border.grid(column=1, row=2)

label_sheets = ttk.Label(frame, text="verso sur bord")
label_sheets.grid(column=0, row=3)
entry_sheets = ttk.Entry(frame, textvariable=vsheets)
entry_sheets.grid(column=1, row=3)

button_ok = ttk.Button(frame, text="OK", command=launch)
button_ok.grid(column=0, row=4)
progress = ttk.Progressbar(frame, orient='horizontal', length=200, mode='determinate')
progress.grid(column=1, row=4)

root.mainloop()
