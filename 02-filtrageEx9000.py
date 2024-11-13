import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, butter, lfilter


gain_1 = 2.0
freq_coupure1 = 20000

freq_basse_2 = 2500 # Fréquence basse de la bande passante en Hz
freq_haute_2 = 5000  # Fréquence haute de la bande passante en Hz
Q_2 = 30.0  # Facteur de qualité
gain_2 = 1.0  # Gain

def filtre_passe_bas1(signal, freq_ech, freq_coupure, gain):

    # Calcul des coefficients du filtre passe-bas de premier ordre
    nyquist = 0.5 * freq_ech
    normal_cutoff = freq_coupure / nyquist
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    
    # Application du filtre au signal
    signal_filtre = lfilter(b, a, signal)* gain
    return signal_filtre

#def filtre_passe_bande(signal, freq_ech, freq_basse, freq_haute, Q, gain=1.0):

#Test à mofidier...
def filtreNumTemp(data):
    a0= 0.4923
    a1= -0.4923
    b1= 0.8763
    b2= -0.1919
    filtered_data = np.zeros_like(data) #Creation donnee sortie meme type que data
   

    filtered_data[0] = a0*data[0]
    filtered_data[1] = a0*data[1] + a1 * data[0] + b1* filtered_data[0]
    filtered_data[2] = a0*data[2] + a1 * data[1] + b1* filtered_data[1] + + b2* filtered_data[0]
     
    for i in range(3, len(data)):
        filtered_data[i] =a0*data[i] + a1 * data[i-1] + b1* filtered_data[i-1] + + b2* filtered_data[i-2]
    return filtered_data




### 3 exemples de donnees d'entress sont proposees
type = 2
creationWavFiltre = False  #True si l'on veut créer un wav à la fin
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
    creationWavFiltre = True
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

# Optionnel : Afficher la magnitude du spectre



# Application du filtre passe-bas
signal_filtre =  filtreNumTemp(data)
#signal_filtre = filtre_passe_bas1(data, freq_ech, freq_coupure1, gain_1)
# Calculer la FFT du signal filtré
fft_result_filtre = np.fft.fft(signal_filtre)



# Écrire le fichier WAV
if creationWavFiltre == True : 
    # Normalisation du signal filtré avec gain
    signal_filtre_normalise = np.clip(signal_filtre, -32768, 32767)  # Limiter les valeurs
    signal_filtre_normalise  = signal_filtre_normalise .astype(np.int16)  # Convertir en entiers 16 bits


    wavfile.write('wav_filtre.wav', freq_ech, signal_filtre_normalise)


# Créer une figure avec deux sous-graphes
plt.figure(figsize=(12, 6))

# Sous-graphe 1 : Signal temporel
plt.subplot(2, 1, 1)
plt.plot(t,data, label='Signal Origine')
plt.plot(t, signal_filtre, label='Signal filtré', linestyle='--')
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude')
plt.title('Signal temporel')



# Sous-graphe 2 : Signal FFT

plt.subplot(2, 1,2)
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result)[:len(fft_result)//2])
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_filtre)[:len(fft_result_filtre)//2])
#plt.plot(frequences[:len(frequences)//2], np.abs(fft_result)[:len(fft_result)//2], label='FFT original')   #on ne visualise que les frequ positive
#plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_filtre)[:len(fft_result_filtre)//2], label='FFT filtré', linestyle='--')
plt.xscale('log')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Magnitude')
plt.title('Spectre de Fourier fin')

# Afficher les sous-graphes
plt.tight_layout()
plt.show()
