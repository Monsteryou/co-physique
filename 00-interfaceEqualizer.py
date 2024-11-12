import tkinter as tk
from tkinter import ttk

# Créer la fenetre principale
root = tk.Tk()
root.title("Slider Simple")
root.geometry("400x600")

# Fonction pour mettre à jour la valeur affichée du slider
def update_value(value):
    print(f"Valeur : {slider.get()}")
    label.config(text=f"Valeur: {int(float(value))}")

def affichageSlider(value):
    print(f"Valeur du slider: {slider.get()}")

# Créer un label pour afficher la valeur du slider
label = ttk.Label(root, text="Valeur: 50")
label.pack(pady=10)


# Créer un slider vertical
slider = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient='vertical',
    length=300,
    command=update_value
)
slider.set(50)  
slider.pack(pady=20)

# Créer un btn
button = ttk.Button(root)
button.pack(pady=20)

# Conf btn
button.config(text="Afficher la valeur", command=affichageSlider)

#Lancement
root.mainloop()