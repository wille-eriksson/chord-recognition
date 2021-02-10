# Author: Wille Eriksson, October 2020

import numpy as np

def get_similarities(chromagram,template):
    """
    Computes and returns the similarity between each frame in chromagram to each of the
    24 major and minor chords as a (24, X) numpy array. Similarity to a chord is computed as the
    scalar product between a frame of the chromagram and the chord's template vector.

    Parameters
    ----------
    chromagram : 2D numpy array of dimensions (12, X)

    template : 2D numpy array of dimensions (24, 12)
    """

    if type(chromagram) != np.ndarray:
        raise TypeError("Chromagram must be 2D numpy ndarray.")

    if type(template) != np.ndarray:
        raise TypeError("Template must be 2D numpy ndarray.")

    if chromagram.shape[0] != 12:
        raise ValueError("Invalid shape of chromagram.")

    if template.shape != (24,12):
        raise ValueError("Invalid shape of chord template.")

    similarities = []

    for c in np.transpose(chromagram):
        similarities.append(np.sum(c*template,axis=1))

    return np.transpose(np.array(similarities))

def get_prediction(similarities):
    """
    Returns decision for the most likely chord at each frame in a given similarity array.

    Parameters
    ----------
    similarities : 2D numpy ndarray of shape (24, X)
    """

    if type(similarities) != np.ndarray:
        raise TypeError("Similarity array must be 2D numpy ndarray.")

    if similarities.shape[0] != 24:
        raise ValueError("Invalid shape of similarity array.")

    max_sim = []
    binary = np.zeros(similarities.shape)

    for frame in np.transpose(similarities):
        max_sim.append(np.argmax(frame))

    for i,chord in enumerate(max_sim):
        binary[chord][i] = 1

    return binary

def temporal_smoothing(chromagram, L = 20):
    """
    Returns a temporal smoothing of input chromagram given a positiv integer L, where each
    frame is given the average value of the L/2 frames before and after it.

    Parameters
    ----------
    chromagram : 2D numpy array of dimensions (12, X)

    L : int
    """
    if type(chromagram) != np.ndarray:
        raise TypeError("Chromagram must be 2D numpy ndarray.")

    if chromagram.shape[0] != 12:
        raise ValueError("Invalid shape of chromagram.")

    if not isinstance(L,int):
        raise TypeError("L must be an integer")

    if (L < 2):
        raise ValueError("L must be an integer larger than 1")


    nframes = chromagram.shape[1]
    avg = []

    for i in range(nframes):
        start = max(0,i-(L-1)//2)
        end = min(i+L//2,nframes-1)

        avg.append(np.sum(np.transpose(chromagram)[start:end],axis=0)/L)

    return np.transpose(np.array(avg))


def log_compression(chromagram,gamma = 1):
    """
    Returns a normalized logarithmic compression of input chromagram given parameter gamma. The logarithmic
    compression of a chromagram C is defined as log(1 + gamma * C).

    Parameters
    ----------
    chromagram : 2D numpy array of dimensions (12, X)

    gamma : int or float
    """

    if type(chromagram) != np.ndarray:
        raise TypeError("Chromagram must be 2D numpy ndarray.")

    if chromagram.shape[0] != 12:
        raise ValueError("Invalid shape of chromagram.")

    if not isinstance(gamma,int) and not isinstance(gamma,float):
        raise TypeError("Gamma must be integer or float.")

    smooth = np.log(1+gamma*chromagram)

    return smooth/np.linalg.norm(smooth, ord=2, axis=0, keepdims=True)

def accuracy(predicted,annotated):
    """
    Given predicted and annotated chords for a soundfile as (24, X) numpy ndarrays returns
    the accuracy of the prediction, i.e. the ratio of correctly predicted chords.

    Parameters
    ----------
    predicted : (24, X) numpy ndarray

    annotated : (24, X) numpy ndarray
    """

    if (type(predicted) != np.ndarray) or (type(annotated) != np.ndarray):
        raise TypeError("Arguments 'predicted' and 'annotated' must be numpy ndarrays.")

    if predicted.shape[0] != 24:
        raise ValueError("Invalid shape of 'predicted'.")

    if annotated.shape[0] != 24:
        raise ValueError("Invalid shape of 'annotated'.")

    if predicted.shape != annotated.shape:
        raise ValueError("Arguments 'predicted' and 'annotated' must have the same shape.")

    nframes = predicted.shape[1]

    annotated_frames = nframes
    equal_frames = 0

    for pred_frame,true_frame in zip(np.transpose(predicted),np.transpose(annotated)):
        if 25 in true_frame:
            annotated_frames -= 1

        if np.array_equal(pred_frame,true_frame):
            equal_frames += 1

    return equal_frames/annotated_frames
