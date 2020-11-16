# 7-Band Audio Equalizer

## Overview

This project is a 7-band audio equalizer implemented in Python using the Tkinter library for the graphical user interface (GUI). Users can select gains for each frequency band and upload a noisy audio file, after which the application processes the audio. It also generates various plots to visualize the effects of the audio equalization.
At the end, an equalised output audio file is generated and saved. 

## Features

- GUI using Tkinter for selecting audio file and adjusting gains for different frequency bands.
- 7 frequency bands for audio equalization:
  - Sub Bass (20-60 Hz)
  - Bass (60-250 Hz)
  - Low Midrange (250-500 Hz)
  - Midrange (500-2000 Hz)
  - Upper Midrange (2000-4000 Hz)
  - Presence (4000-6000 Hz)
  - Brilliance (6000-20000 Hz)
- Visualizations plots for the original input and equalized audio signal like Time-domain waveforms, Frequency response plots, Spectrogram
- Output equalized audio signal saved as a new WAV file.

## Requirements

- Python 3.x
- Required libraries:NumPy, librosa, SciPy, SoundFile, Matplotlib, Tkinter, SoundDevice

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/vedaantdutt/7-band-audio-equaliser.git
   cd 7-band-audio-equaliser
   ```

2. Create a virutal environment
   ```
   python -m venv venv
   ```

3. Activate the virtual environment
   ```
   venv\Scripts\activate
   ```

4. Install the libraries:
   ```
   pip install numpy librosa scipy soundfile matplotlib sounddevice 
   ```

## Usage

1. Run the python file:
   ```
   python audio_equaliser.py
   ```
2. In the GUI:
   1. Click on the "Select Audio File" button to upload a noisy audio file in the WAV format.
   2. Adjust the sliders for each frequency band to set the gains.
   3. Finally, click the "Process" button to process the audio and generate plots.
   After processing, firstly the plots are generated. Then, the equalized audio will be saved as equalised_<input-filename>.wav in the same directory.

## Future Improvements
- Real-time audio processing.
- Support for additional audio formats like mp3 etc
- using filters characteristics and filters other than butterworth.

