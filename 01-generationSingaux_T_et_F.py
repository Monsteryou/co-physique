import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


### 3 exemples de donnees d'entress sont proposees

type = 1

if type == 0 : 
    ###### Signal sinusoïdal
    freq_ech = 44100  # Fréquence d'échantillonnage en Hz
    f_sin = 2000  # Fréquence du signal sinusoïdal en Hz
    duree = 1      # Durée du signal en secondes
    # Créer un tableau de temps
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)
    # Générer le signal sinusoïdal
    data = np.sin(2 * np.pi * f_sin * t)
    ###### fin signal sinusoïdal

elif type == 1 : 
    ####### Fichier wav lu resultat dans u ntableau (attention au mon ou au stéréo
    freq_ech, data = wavfile.read('LW_20M_amis.wav')
    # Créer un tableau de temps
    t = np.linspace(0, len(data) / freq_ech, len(data), endpoint=False)
    ####### Fin wav
else : 
    ##### Une impulsion
    freq_ech = 44100
    duree = 3
    data = np.zeros(freq_ech*duree)
    data[0] = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)
    #####Fin impulsion



# Vérifier si le fichier est stéréo ou mono
if len(data.shape) > 1:
    # Si le fichier est stéréo, prendre un seul canal (par exemple, le canal gauche)
    data = data[:, 0]

# Appliquer la FFT
fft_result = np.fft.fft(data)

# Creation du vecteur frequence 1re moitier freq positive, 2e moitié freq négative.  
frequences = np.fft.fftfreq(len(fft_result), d=1/freq_ech)  
print(frequences)
print(len(frequences))



# Créer une figure avec deux sous-graphes
plt.figure(figsize=(12, 6))

# Sous-graphe 1 : Signal temporel
plt.subplot(2, 1, 1)
plt.plot(t,data)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude')
plt.title('Signal sinusoïdal 3000 Hz (Signal temporel)')



# Sous-graphe 2 : Signal FFT
plt.subplot(2, 1,2)
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result)[:len(fft_result)//2])   #on ne visualise que les frequ positive
plt.xscale('log')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Magnitude')
plt.title('Spectre de Fourier')

# Afficher les sous-graphes
plt.tight_layout()
plt.show()