import numpy as np
import math

def find_nearest(arr: np.array, value: float) -> int:
    '''
    Finds the nearest element to the input value in the array
    '''
    idx = np.searchsorted(arr, value, side="left")
    if idx > 0 and (idx == len(arr) or math.fabs(value - arr[idx-1]) < math.fabs(value - arr[idx])):
        return idx
    else:
        return idx
    
def find_peak(arr: np.array, i: int, j: int, k: int) -> int:
    '''
    Finds the peak in the 2D array within given 1D segment
    Specifically used for finding the bad coupling channels in magnitude spectra
    '''
    seg = np.log10(arr[i,j:k]) # Slice the array into a line segment
    peak = int(np.where(seg == np.amax(seg))[0])
    print(j+peak)
    return j+peak