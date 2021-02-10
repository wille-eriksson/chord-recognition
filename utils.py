# Author: Wille Eriksson, October 2020

"""
File containing the labels of chords and pitch classes, as well as utility functions
for template based chord recognition.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.cm import get_cmap
from annotations import Ipanema, HoneyHoney, HelterSkelter
from copy import deepcopy
from chordrec import accuracy

pitchclass_labels = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

chord_labels = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B","Cm","C#m","Dm","D#m","Em","Fm","F#m","Gm","G#m","Am","A#m","Bm"]

def plot_chromagram(chromagram, hopsize, title = ""):
    """
    Provides a correctly formated plot of a chromagram,
    given said chromagram and its hopsize in seconds.

    Parameters
    ----------
    chromagram : 2D numpy array with shape (12, X)

    hopsize : float

    title : string (Optional)
    """

    if chromagram.shape[0] != 12:
        raise ValueError("Invalid shape for a chromagram.")

    nframes = chromagram.shape[1] # Obtain the number of frames in the chromagram

    time = np.linspace(0, nframes * hopsize, nframes + 1) # Create time vector for plotting
    int_pitches = np.arange(13) # Integer values for y-axis

    plt.pcolormesh(time, int_pitches, chromagram, vmin = 0, vmax = np.max(chromagram),cmap = "Greys")

    plt.xlabel("Time (s)", fontsize = 20)
    plt.ylabel("Pitch class", fontsize = 20)
    plt.yticks(np.arange(12)+0.5, pitchclass_labels)

    if title != "":
        plt.title(title, fontsize = 25, pad = 20)

    plt.show()

def plot_similarities(sim, hopsize, annotated = None, title = ""):
    """
    Provides a correctly formated plot of 2D array describing the similarities between a
    chromagram and the 24 major and minor chords, given said array and the hopsize of the
    chormagram in seconds.

    Parameters
    ----------
    sim : 2D numpy array with shape (24, X)

    hopsize : float

    title : string (Optional)
    """

    if sim.shape[0] != 24:
        raise ValueError("Invalid shape for a similarity array.")

    nframes = sim.shape[1] # Obtain the number of frames in the chromagram
    time = np.linspace(0, nframes * hopsize, nframes + 1) # Create time vector for plotting
    int_chords = np.arange(25) # Integer values for y-axis


    plt.pcolormesh(time, int_chords, sim, cmap = "Greys")

    plt.xlabel("Time (s)", fontsize = 20)
    plt.ylabel("Chord", fontsize = 20)
    plt.yticks(np.arange(24)+0.5, chord_labels)

    if title != "":
        plt.title(title, fontsize = 25, pad = 20)

    plt.show()

def plot_predicted(predicted, hopsize, annotated = None, title = ""):
    """
    Provides a correctly formated plot of 2D array describing the predicted chords of an audiofile,
    given said array and the hopsize of the STFT used in seconds. Optionally, annotated chords for
    the audiofile may also be displayed in the plot if these are given as a 2D array.

    Parameters
    ----------
    predicted : 2D numpy array with shape (24, X)

    hopsize : float

    annotated: 2D numpy array with shape (24, X) (Optional)

    title : string (Optional)
    """

    if predicted.shape[0] != 24:
        raise ValueError("Invalid shape for a predicted similarity array.")

    pred_col = 'Greys'
    ann_col = 'Reds'

    nframes = predicted.shape[1] # Obtain the number of frames in the chromagram
    time = np.linspace(0, nframes * hopsize, nframes + 1) # Create time vector for plotting
    int_chords = np.arange(25) # Integer values for y-axis

    if annotated is not None:
        ann_col_str = 0.6
        pred_col_str = 1.0

        ann_copy = deepcopy(annotated)
        ann_copy[ann_copy == 0] = np.nan
        plt.pcolormesh(time, int_chords, ann_copy*ann_col_str,vmin = 0, vmax = 1, cmap = ann_col)

        acc = round(accuracy(predicted, annotated),2)

        plt.legend(handles = [Patch(color = get_cmap(pred_col)(pred_col_str), label = "Predicted"),
                              Patch(color = get_cmap(ann_col)(ann_col_str), label = "Annotated"),
                              Patch(label = 'Accuracy = ' + str(acc), alpha = 0.0)],
                              fontsize = "large")

    pred_copy = deepcopy(predicted)
    pred_copy[pred_copy == 0] = np.nan

    plt.pcolormesh(time, int_chords, pred_copy, cmap = pred_col,vmin = 0, vmax = 1)

    plt.xlabel("Time (s)", fontsize = 20)
    plt.ylabel("Chord", fontsize = 20)
    plt.yticks(np.arange(24)+0.5, chord_labels)

    if title != "":
        plt.title(title, fontsize = 25, pad = 20)

    plt.show()

def get_chord_template(alpha = 0.0):
    """
    Returns template with harmonic consideration for all 24 major and minor chords as a (24,12) numpy array,
    given an input weight alpha.

    Parameters
    ----------
    alpha : float
    """

    if not isinstance(alpha,float or int):
        raise TypeError("Alpha must be float or integer between 0 and 1.")

    if alpha < 0:
        raise ValueError("Alpha cannot be negative.")

    elif alpha > 1:
        raise ValueError("Alpha should be between 0 and 1.")

    root = np.zeros(12)

    root[0] = 1 + alpha + alpha ** 3 + alpha ** 7
    root[4] = alpha ** 4
    root[7] = alpha ** 2 + alpha ** 5
    root[10] = alpha ** 6

    min_third = np.concatenate((root[-3:],root[:-3]))
    maj_third = np.concatenate((root[-4:],root[:-4]))
    fifth = np.concatenate((root[-7:],root[:-7]))

    major_chord = root + maj_third + fifth
    minor_chord = root + min_third + fifth

    norm = np.linalg.norm(major_chord)

    template = np.zeros((24,12))

    for i in range(12):
        template[i] = np.concatenate((major_chord[-i:],major_chord[:-i]))/norm
        template[i+12] = np.concatenate((minor_chord[-i:],minor_chord[:-i]))/norm

    return template

def get_annotations(title,nframes):
    """
    Provides the annotated chords over time for the first 30 seconds of the songs
    "The girl from Ipanema", "Honey Honey" and "Helter Skelter" in the form of
    (24,X) numpy ndarrays, in the purpose of testing the performence of the chord
    recognizer. Valid inputs for "title" are the strings "Ipanema", "HoneyHoney" and
    "HelterSkelter". Number of frames in the chromagram used for computations must be
    entered as an integer in argument nframes.

    Parameters
    ----------
    title : str

    nframes : int
    """

    library = {"HelterSkelter" : HelterSkelter,
               "Ipanema" : Ipanema,
               "HoneyHoney" : HoneyHoney}

    if not isinstance(title,str):
        raise TypeError("Argument 'title' must be string.")

    if title not in [*library]:
        raise ValueError("Argument 'title' must be one of the strings 'HelterSkelter', 'Ipanema' or 'HoneyHoney'.")

    if not isinstance(nframes,int):
        raise TypeError("Argument hopsize must be float.")

    song = library[title]
    keys = [*song]

    annotated = np.zeros((24,nframes))

    time = np.linspace(0,30,nframes)

    for i,t in enumerate(time):
        for key,next_key in zip(keys[:-1],keys[1:]):

            if key < t <= next_key:

                true_chord = song[key]

                if true_chord == 25:
                    pass

                else:
                    annotated[true_chord][i] = 1
                break

    return annotated
