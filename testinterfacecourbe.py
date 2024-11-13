import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings

# Ignorer les avertissements spécifiques de WavFileWarning
warnings.filterwarnings("ignore", category=wavfile.WavFileWarning)

def apply_filter(data, a0, a1, b1, b2):
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    for i in range(2, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i-1] + b1 * filtered_data[i-1] + b2 * filtered_data[i-2]
    return filtered_data

def filtreNumTemp1(data): return apply_filter(data, 0.2183, -0.2183, 1.7505, -0.7661)
def filtreNumTemp3(data): return apply_filter(data, 0.419, -0.4195, 1.4011, -0.4907)
def filtreNumTemp5(data): return apply_filter(data, 0.4858, -0.4858, 1.1679, -0.3410)
def filtreNumTemp7(data): return apply_filter(data, 0.4999, -0.4999, 1.0013, -0.2506)
def filtreNumTemp9(data): return apply_filter(data, 0.4923, -0.4923, 0.8763, -0.1919)

class AudioEqualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Égaliseur Audio avec Visualisation et Coniques")
        self.master.geometry("1200x1000")

        self.data = None
        self.freq_ech = None
        self.fig = None
        self.canvas = None
        self.ax1, self.ax2, self.ax3 = None, None, None

        self.slider_values = [tk.DoubleVar() for _ in range(5)]
        for var in self.slider_values:
            var.trace_add('write', self.update_curves)

        self.create_widgets()

    def create_widgets(self):
        file_button = ttk.Button(self.master, text="Sélectionner un fichier WAV", command=self.select_file)
        file_button.pack(pady=10)

        self.slider_frame = tk.Frame(self.master)
        self.slider_frame.pack()

        self.sliders = []
        self.band_labels = []

        for i in range(5):
            band_frame = tk.Frame(self.slider_frame)
            band_frame.pack(side='left', padx=10)
            
            slider = ttk.Scale(
                band_frame,
                from_=-10,
                to=10,
                orient='vertical',
                length=200,
                variable=self.slider_values[i]
            )
            self.sliders.append(slider)
            slider.pack()
            
            label = ttk.Label(band_frame, text=f"Bande{i}: 0")
            self.band_labels.append(label)
            label.pack()

            self.slider_values[i].trace_add('write', lambda *args, index=i: self.update_label(index))

    def update_label(self, index):
        value = self.slider_values[index].get()
        self.band_labels[index].config(text=f"Bande{index}: {int(value)}")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            try:
                # Utilisation de wavfile.read avec gestion des avertissements
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", wavfile.WavFileWarning)
                    self.freq_ech, self.data = wavfile.read(file_path)
                
                if len(self.data.shape) > 1:
                    self.data = self.data[:, 0]  # Prendre seulement le canal gauche si stéréo
                print("Fichier sélectionné:", file_path)
                self.create_plot()
                self.update_curves()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier: {str(e)}")

    def create_plot(self):
        if hasattr(self, 'fig') and self.fig:
            plt.close(self.fig)
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 12))
        
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_curves(self, *args):
        if self.data is None or not hasattr(self, 'fig') or self.fig is None:
            return

        slider_values = [var.get() for var in self.slider_values]
        
        fft_result = np.fft.fft(self.data)
        frequences = np.fft.fftfreq(len(fft_result), d=1/self.freq_ech)
        
        filters = [filtreNumTemp1, filtreNumTemp3, filtreNumTemp5, filtreNumTemp7, filtreNumTemp9]
        filtered_signals = [filter_func(self.data) * (10 ** (value / 20)) for filter_func, value in zip(filters, slider_values)]
        
        combined_signal = np.sum(filtered_signals, axis=0)
        fft_combined = np.fft.fft(combined_signal)
        
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        # Signal audio dans le domaine temporel
        t = np.linspace(0, len(self.data)/self.freq_ech, len(self.data), endpoint=False)
        self.ax1.plot(t, self.data, label='Original', alpha=0.5)
        self.ax1.plot(t, combined_signal, label='Filtré', color='red')
        self.ax1.set_xlabel('Temps [s]')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.set_title('Signal dans le domaine temporel')
        self.ax1.legend()
        
        # Signal audio dans le domaine fréquentiel
        self.ax2.semilogx(frequences[:len(frequences)//2], 20*np.log10(np.abs(fft_result[:len(fft_result)//2]) + 1e-10), 
                     label='Original', alpha=0.5)
        self.ax2.semilogx(frequences[:len(frequences)//2], 20*np.log10(np.abs(fft_combined[:len(fft_combined)//2]) + 1e-10), 
                     label='Filtré', color='red')
        self.ax2.set_xlabel('Fréquence [Hz]')
        self.ax2.set_ylabel('Magnitude [dB]')
        self.ax2.set_title('Spectre de fréquence')
        self.ax2.legend()
        
        # Courbes de type 2 (coniques)
        x = np.linspace(-5, 5, 1000)
        
        # Ellipse
        a, b = 3, 2
        y_ellipse = b * np.sqrt(1 - (x/a)**2)
        self.ax3.plot(x, y_ellipse, 'b-', label='Ellipse')
        self.ax3.plot(x, -y_ellipse, 'b-')
        
        # Parabole
        y_parabole = x**2 / 4
        self.ax3.plot(x, y_parabole, 'g-', label='Parabole')
        
        # Hyperbole
        y_hyperbole = np.sqrt((x/a)**2 - 1) * b
        self.ax3.plot(x[x <= -a], y_hyperbole[x <= -a], 'r-', label='Hyperbole')
        self.ax3.plot(x[x <= -a], -y_hyperbole[x <= -a], 'r-')
        self.ax3.plot(x[x >= a], y_hyperbole[x >= a], 'r-')
        self.ax3.plot(x[x >= a], -y_hyperbole[x >= a], 'r-')
        
        self.ax3.set_xlim(-5, 5)
        self.ax3.set_ylim(-5, 5)
        self.ax3.set_xlabel('x')
        self.ax3.set_ylabel('y')
        self.ax3.set_title('Courbes de type 2 (Coniques)')
        self.ax3.legend()
        self.ax3.grid(True)
        
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioEqualizer(root)
    root.mainloop()