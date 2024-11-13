import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Define the filter functions
def filtreNumTemp1(data):
    a0= 0.2183
    a1= -0.2183
    b1= 1.7505
    b2= -0.7661
    filtered_data = np.zeros_like(data)
    
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    
    for i in range(2, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp3(data):
    a0= 0.419
    a1= -0.4195
    b1= 1.4011
    b2= -0.4907
    filtered_data = np.zeros_like(data)
    
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    
    for i in range(2, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp5(data):
    a0= 0.4858
    a1= -0.4858
    b1= 1.1679
    b2= -0.3410
    
    filtered_data = np.zeros_like(data)
    
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    
    for i in range(2, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp7(data):
    a0= 0.4999
    a1= -0.4999
    b1= 1.0013
    b2= -0.2506
    filtered_data = np.zeros_like(data)
    
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    
    for i in range(2, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp9(data):
    a0= 0.4923
    a1= -0.4923
    b1= 0.8763
    b2= -0.1919
    filtered_data = np.zeros_like(data)
    
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    
    for i in range(2, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

# Example data processing
type = 2
creationWavFiltre = False  # Set True to create a wav file at the end
if type == 0:
    # Sinusoidal signal
    freq_ech = 96000
    f_sin = 100
    duree = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)
    data = np.sin(2 * np.pi * f_sin * t)
elif type == 1:
    # WAV file
    freq_ech, data = wavfile.read('LW_20M_amis.wav')
    t = np.linspace(0, len(data) / freq_ech, len(data), endpoint=False)
    creationWavFiltre = True
else:
    # Impulse
    freq_ech = 96000
    duree = 1
    data = np.zeros(freq_ech * duree)
    data[0] = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)

# Mono check
if len(data.shape) > 1:
    data = data[:, 0]

# FFT calculation
fft_result = np.fft.fft(data)
frequences = np.fft.fftfreq(len(fft_result), d=1 / freq_ech)

# Apply each filter and store results for plotting
filters = [filtreNumTemp1, filtreNumTemp3, filtreNumTemp5, filtreNumTemp7, filtreNumTemp9]
filter_labels = ['Filtre 1', 'Filtre 3', 'Filtre 5', 'Filtre 7', 'Filtre 9']
styles = ['-', '--', '-.', ':', '-']
filtered_signals = []
fft_filtered_signals = []

for filter_func in filters:
    filtered_signal = filter_func(data)
    filtered_signals.append(filtered_signal)
    fft_filtered_signals.append(np.fft.fft(filtered_signal))

# Plotting
plt.figure(figsize=(12, 10))

# Time-domain signal
plt.subplot(2, 1, 1)
plt.plot(t, data, label='Original Signal', color='black')
for i, filtered_signal in enumerate(filtered_signals):
    plt.plot(t, filtered_signal, styles[i], label=filter_labels[i])
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Time-Domain Signal')
plt.legend()

# Frequency-domain signal
plt.subplot(2, 1, 2)
plt.plot(frequences[:len(frequences) // 2], np.abs(fft_result)[:len(fft_result) // 2], label='Original FFT', color='black')
for i, fft_signal in enumerate(fft_filtered_signals):
    plt.plot(frequences[:len(frequences) // 2], np.abs(fft_signal)[:len(fft_signal) // 2], styles[i], label=filter_labels[i])
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Frequency-Domain Signal')
plt.legend()

plt.tight_layout()
plt.show()
