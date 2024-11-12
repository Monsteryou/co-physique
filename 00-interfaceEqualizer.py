import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Créer la fenêtre principale
root = tk.Tk()
root.title("Égaliseur Simple")
root.geometry("400x500")

# Fonction pour mettre à jour la valeur affichée de chaque slider
def update_value(value, band_index):
    band_labels[band_index].config(text=f"Bande{band_index}: {int(float(value))}")

# Fonction pour afficher la valeur de chaque slider lors du traitement
def process_audio():
    slider_values = [slider.get() for slider in sliders]
    print("Valeurs des sliders:", slider_values)
    # Le traitement audio pourrait être ajouté ici

# Créer un bouton pour sélectionner un fichier WAV
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    print("Fichier sélectionné:", file_path)

# Bouton pour sélectionner un fichier
file_button = ttk.Button(root, text="Sélectionner un fichier WAV", command=select_file)
file_button.pack(pady=10)

# Frame pour organiser les sliders et leurs labels
slider_frame = tk.Frame(root)
slider_frame.pack()

# Créer une liste pour les sliders et les labels de bandes
sliders = []
band_labels = []

# Créer 5 sliders avec labels
for i in range(5):
    # Frame pour chaque slider et son label
    band_frame = tk.Frame(slider_frame)
    band_frame.pack(side='left', padx=10)
    
    # Créer un slider vertical
    slider = ttk.Scale(
        band_frame,
        from_=-10,
        to=10,
        orient='vertical',
        length=200,
        command=lambda value, idx=i: update_value(value, idx)
    )
    slider.set(0)
    sliders.append(slider)
    slider.pack()
    
    # Créer un label sous chaque slider
    label = ttk.Label(band_frame, text=f"Bande{i}: 0")
    band_labels.append(label)
    label.pack()

# Créer un bouton pour effectuer le traitement, en dessous des sliders
process_button = ttk.Button(root, text="Effectuer le traitement", command=process_audio)
process_button.pack(pady=20)

# Lancement de la boucle principale
root.mainloop()
