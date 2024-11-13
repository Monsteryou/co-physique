import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile
import threading
import sounddevice as sd

# Créer la fenêtre principale
root = tk.Tk()
root.title("Égaliseur Simple")
root.geometry("800x600")

# Variables globales pour stocker les données audio
sample_rate = None
audio_data = None
modified_audio = None
fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()

# Fonction pour mettre à jour l'étiquette de la valeur du curseur
def update_value(value, band_index):
    band_labels[band_index].config(text=f"Bande{band_index}: {int(float(value))}")

# Fonction pour sélectionner un fichier audio
def select_file():
    global sample_rate, audio_data
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        sample_rate, audio_data = wavfile.read(file_path)
        print("Fichier sélectionné:", file_path)
        threading.Thread(target=plot_curves).start()

# Fonction pour tracer les courbes des filtres appliqués en fonction du temps
def plot_curves():
    global modified_audio
    if audio_data is None:
        return

    ax.clear()
    time = np.arange(len(audio_data)) / sample_rate  # Calcul du temps en secondes pour l'axe x
    
    # Utilisation d'un échantillonnage pour alléger la courbe si le fichier est trop long
    if len(time) > 50000:  # Ajustez ce seuil selon la performance
        step = len(time) // 50000  # Limiter à 50 000 points
        time = time[::step]
        audio_plot = audio_data[::step]
    else:
        audio_plot = audio_data
    
    ax.plot(time, audio_plot, label='Original', color='blue', alpha=0.6, linewidth=1)

    # Liste des filtres
    filters = [filtreNumTemp1, filtreNumTemp3, filtreNumTemp5, filtreNumTemp7, filtreNumTemp9]
    labels = ['Bande 1', 'Bande 3', 'Bande 5', 'Bande 7', 'Bande 9']
    colors = ['orange', 'green', 'red', 'purple', 'brown']  # Couleurs contrastées

    # Signal modifié combiné
    modified_audio = np.zeros_like(audio_data, dtype=float)

    for filter_func, label, slider, color in zip(filters, labels, sliders, colors):
        gain = slider.get()
        filtered = filter_func(audio_data)
        amplified = filtered * (10 ** (gain / 20))  # Application du gain en dB
        modified_audio += amplified
        # Afficher la courbe en fonction du temps avec un style lisible
        ax.plot(time, amplified[::step], label=f'{label} (Gain: {gain})', color=color, linewidth=1.5)

    # Paramètres d'affichage du graphique
    ax.set_xlabel('Temps (s)')  # Étiqueter l'axe des x comme le temps
    ax.set_ylabel('Amplitude')
    ax.set_title('Courbes des filtres appliqués (domaine temporel)')

    # Légende ajustée
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small', frameon=True)

    # Amélioration de la présentation générale
    ax.grid(True, linestyle='--', alpha=0.7)
    
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Fonction pour appliquer les réglages des curseurs et mettre à jour les courbes
def process_audio():
    global modified_audio
    threading.Thread(target=plot_curves).start()
    # Attendre que le traitement soit terminé
    while modified_audio is None:
        root.update()

# Fonction pour jouer le son modifié
def play_audio():
    global modified_audio, sample_rate
    if modified_audio is not None and sample_rate is not None:
        # Normaliser l'audio pour éviter les distorsions
        normalized_audio = np.int16(modified_audio / np.max(np.abs(modified_audio)) * 32767)
        # Jouer l'audio
        sd.play(normalized_audio, sample_rate)
        sd.wait()

# Bouton pour enregistrer le fichier audio modifié
def save_modified_audio():
    if modified_audio is not None:
        save_path = r"C:\Users\CIEL23_admin\Documents\2024-2025\co_physique\seq00-modificationsSonors\act00-interfaceModificationsSonore\ressource_eleve\audio_modifié.wav"
        
        # Normalisation du signal pour éviter les coupures et mise à l'échelle dans l'intervalle int16
        max_amplitude = np.max(np.abs(modified_audio))
        if max_amplitude > 0:
            scaled_audio = modified_audio / max_amplitude  # Normalisation
            scaled_audio = np.int16(scaled_audio * 32767)  # Conversion en int16
        else:
            scaled_audio = np.int16(modified_audio)

        # Enregistrement du fichier WAV modifié
        wavfile.write(save_path, sample_rate, scaled_audio)
        print(f"Fichier audio modifié enregistré à : {save_path}")

# Bouton pour sélectionner un fichier WAV
file_button = ttk.Button(root, text="Sélectionner un fichier WAV", command=select_file)
file_button.pack(pady=10)

slider_frame = tk.Frame(root)
slider_frame.pack()

# Liste pour stocker les curseurs et les étiquettes de bande
sliders = []
band_labels = []

for i in range(5):
    band_frame = tk.Frame(slider_frame)
    band_frame.pack(side='left', padx=10)
    
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
    
    label = ttk.Label(band_frame, text=f"Bande{i}: 0")
    band_labels.append(label)
    label.pack()

# Bouton "Effectuer le traitement"
process_button = ttk.Button(root, text="Effectuer le traitement", command=process_audio)
process_button.pack(pady=20)

# Bouton "Enregistrer les modifications"
save_button = ttk.Button(root, text="Enregistrer les modifications", command=save_modified_audio)
save_button.pack(pady=10)

# Fonction de filtre numérique
def apply_filter(data, a0, a1, b1, b2):
    filtered_data = np.zeros_like(data, dtype=float)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    for i in range(2, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp1(data):
    return apply_filter(data, 0.2183, -0.2183, 1.7505, -0.7661)

def filtreNumTemp3(data):
    return apply_filter(data, 0.419, -0.4195, 1.4011, -0.4907)

def filtreNumTemp5(data):
    return apply_filter(data, 0.4858, -0.4858, 1.1679, -0.3410)

def filtreNumTemp7(data):
    return apply_filter(data, 0.4999, -0.4999, 1.0013, -0.2506)

def filtreNumTemp9(data):
    return apply_filter(data, 0.4923, -0.4923, 0.8763, -0.1919)

root.mainloop()