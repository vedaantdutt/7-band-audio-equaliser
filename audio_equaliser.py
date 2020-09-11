
import numpy as np
import librosa
import scipy.signal as signal
import soundfile as sf
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pdb
from pathlib import Path
import sounddevice as sd

#contains audio file path
filePath=None
fileName=None


#function to plot frequency response
def plot_frequency_response_fft(sig, sampleRate, title):

    n = len(sig)

    #Fast fourier transform
    #calculating amplitude
    fftVals = np.fft.fft(sig)

    #frequency axis
    fftFreqs = np.fft.fftfreq(n, 1 / sampleRate)

    #amplitude absolute at each frequency
    magnitude = np.abs(fftVals)

    #plotting only the positive frequencies
    #"plt.plot(fftFreqs, magnitude)
    plt.plot(fftFreqs[:n // 2], magnitude[:n // 2])

    plt.title(title)
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Magnitude')
    plt.grid()


# function to equalize audio
def equalize_audio(sig, sampleRate, gains):

    # deifining bands
    bands = {
        'sub_bass': (20, 60),
        'bass': (60, 250),
        'low_midrange': (250, 500),
        'midrange': (500, 2000),
        'upper_midrange': (2000, 4000),
        'presence': (4000, 6000),
        'brilliance': (6000, 20000)
    }
    
    filteredSignals = {}
    
    #Plotting frequency response
    # plt.figure(figsize=(12, 10))
    # plt.suptitle('Frequency Response of Bandpass Filters for each band')

    i=1
    #skip=0
    plt.figure(figsize=(12, 10))

    for (bandName, (lowCut, highCut)) in bands.items():

         #window function
         window = np.hamming(len(sig))
         windowedSig = sig * window

         #nyquist frequency
         nyquist = 0.5 * sampleRate

         #low cutoff frequency
         low = lowCut / nyquist

         #high cutoff frequency
         high = highCut / nyquist

         #filter order
         order=4

         #obtaining filter coefficients of bandpass butter filter
         b, a = signal.butter(order, [low, high], btype='band')

         #applying filter to the signal
         filteredSignal = signal.lfilter(b, a, windowedSig)
        
         #skip if there are any NaN values
         if np.isnan(filteredSignal).any():
            print(f"Skipping {bandName} band as few values were not found")
           # skip=skip+1
            continue

         #plotting freqeuncy response of each band
         plt.subplot(3, 3, i)
         plot_frequency_response_fft(filteredSignal, sampleRate, f'{bandName} Band ({lowCut}-{highCut} Hz)')
        
         #applying gain
         filteredSignals[bandName] = filteredSignal * gains[bandName]

         i=i+1
    
    # plt.tight_layout(rect=[0, 0, 1, 1])
    plt.subplots_adjust(wspace=0.4, hspace=0.4) 
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    #sum of all bands
    equalizedSignal = sum(filteredSignals.values())

    #plotting freqeuncy response of equalised signal
    plt.figure(figsize=(12, 6))
    plot_frequency_response_fft(equalizedSignal, sampleRate, 'Frequency Response of Equalized Signal')
    
    return equalizedSignal


def plot_spectrogram(sig, sampleRate, title):

    # plt.figure(figsize=(12, 6))
    plt.specgram(sig, Fs=sampleRate, NFFT=2048, noverlap=1024, cmap='viridis')
    plt.title(title)
    plt.xlabel('Time(s)')
    plt.ylabel('Frequency(Hz)')
    plt.colorbar(label='Intensity(dB)')
    plt.grid()


def process_audio():
    global filePath

    if not filePath:
        messagebox.showerror("Error", "No audio file selected.")
        return
    
    # Collect gain values from the GUI sliders
    gains = {
        'sub_bass': subBassGain.get(),
        'bass': bassGain.get(),
        'low_midrange': lowMidrangeGain.get(),
        'midrange': midrangeGain.get(),
        'upper_midrange': upperMidrangeGain.get(),
        'presence': presenceGain.get(),
        'brilliance': brillianceGain.get()
    }
    
    # close the GUI window
    root.destroy()

    # Load and process audio noisy signal
    try:
    #  global filePath
     #noisySignal, sampleRate = librosa.load('noisy_bird_chirping.wav', sr=None)
     noisySignal, sampleRate = librosa.load(filePath, sr=None)

    except FileNotFoundError:
        messagebox.showerror("Error", "Audio file not found.")
        return
    

    # check if signal is empty
    if noisySignal.size > 0:

        #removing dc component
        noisySignal=noisySignal-np.mean(noisySignal)

        #plotting time domain of noisy signal
        duration = len(noisySignal) / sampleRate  
        time = np.linspace(0, duration, len(noisySignal)) 
        plt.figure(figsize=(12,6))
        plt.plot(time,noisySignal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Time Domain of Original Noisy Signal")
        

        #plotting frequency response of noisy signal
        plt.figure(figsize=(12, 6))
        #plt.subplot(2, 1, 1)
        plot_frequency_response_fft(noisySignal, sampleRate, 'Frequency Response of Original Noisy Signal')
        #print(noisySignal)

        equalizedSignal = equalize_audio(noisySignal, sampleRate, gains)
        
        # Save processed audio
        sf.write('equalised_'+fileName, equalizedSignal, sampleRate)

        # Plot spectrograms
        plt.figure(figsize=(12, 8))
        #plt.subplot(2, 1, 1)
        plot_spectrogram(noisySignal, sampleRate, 'Spectrogram of Original Noisy Signal')

        #plt.subplot(2, 1, 2)
        #plot_spectrogram(equalizedSignal, sampleRate, 'Spectrogram of Equalised Signal')
        
        plt.tight_layout()
        #plt.Show()
        plt.show()

        #message box displaying success message
        messagebox.showinfo("Success", "Equalized audio successfully saved")
    
    else:
        messagebox.showerror("Error", "Input audio signal is empty")



def load_audio_file():

    global filePath
    global fileName

    filePath = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])

    if filePath:
        fileName = filePath.split('/')[-1] 
        print(f"Loaded file: {fileName}")
        # selectFileButton.setEnabled(False)
        selectFileButton.config(state=tk.DISABLED)
        processButton.config(state=tk.NORMAL)
        label.config(text=fileName)


#GUI window
root = tk.Tk()
root.geometry("800x700")
root.title("7-Band Audio Equaliser")

# Length of slider
sliderLength = 600  

selectFileButton = tk.Button(root, text="Select Audio File", command=lambda: load_audio_file())
selectFileButton.pack(pady=10)
selectFileButton.pack()


label=tk.Label(root)
label.pack(pady=10)
label.pack()

subBassGain = tk.Scale(root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=sliderLength, label="Sub Bass (20-60 Hz)")
subBassGain.set(1)
subBassGain.pack(pady=10)

bassGain = tk.Scale(root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=sliderLength, label="Bass(60-250 Hz)")
bassGain.set(1)
bassGain.pack(pady=10)

lowMidrangeGain = tk.Scale(root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=sliderLength, label="Low Midrange (250-500 Hz)")
lowMidrangeGain.set(1)
lowMidrangeGain.pack(pady=10)

midrangeGain = tk.Scale(root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=sliderLength, label="Midrange (500-2000 Hz)")
midrangeGain.set(1)
midrangeGain.pack(pady=10)

upperMidrangeGain = tk.Scale(root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=sliderLength, label="Upper Midrange (2000-4000 Hz)")
upperMidrangeGain.set(1)
upperMidrangeGain.pack(pady=10)

presenceGain = tk.Scale(root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=sliderLength, label="Presence. (4000-6000 Hz)")
presenceGain.set(1)
presenceGain.pack(pady=10)

brillianceGain = tk.Scale(root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=sliderLength, label="Brilliance (6000-20000 Hz)")
brillianceGain.set(1)
brillianceGain.pack(pady=10)

#processButton = tk.Button(root, text="Process", command=process_audio)
processButton = tk.Button(root, text="Process", command=process_audio,state="disabled")
processButton.pack(pady=20)


# Tkinter event loop
root.mainloop()