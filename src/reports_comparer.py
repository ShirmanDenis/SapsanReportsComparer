from sapsan_results import SapsanResult
import numpy as np
import math
from scipy.stats import ks_2samp, mannwhitneyu
import matplotlib.pyplot as plt
from statsmodels.tsa.api import SimpleExpSmoothing
from datetime import datetime

class ReportsComparer:
    def __init__(self, s1: SapsanResult, s2: SapsanResult):
        self.s1 = s1
        self.s2 = s2
    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w
    def __smooth(self, prev, current):
        a = 0.7 #1 - math.exp(-1 / 10)
        return a * current + (1 - a) * prev
    def __sm(self, array):
        s = []
        for i in range(1, len(array)):
            s.append(self.__smooth(array[i - 1], array[i]))
        return s
    def compare_percentiles(self):
        results = []
        p1 = self.s1.get_avg_latency()
        p2 = self.s2.get_avg_latency()
        if (len(p1) != len(p2)):
            raise Exception("Percentiles have different dimensions.")
        for i in range(0, len(p1)):
            curr_p1 = p1[i][2]
            curr_p2 = p2[i][2]
            min_length = min(len(curr_p1), len(curr_p2))
            if len(curr_p1) == min_length:
                curr_p2 = curr_p2[:min_length]
            else:
                curr_p1 = curr_p1[:min_length]
            last_count = min_length - 3*60
            smoothed1 = self.moving_average(curr_p1[-last_count:], 10)
            x1 = [i for i in range(0, len(smoothed1))]
            smoothed2 = self.moving_average(curr_p2[-last_count:], 10)
            x2 = [i for i in range(0, len(smoothed2))]
            plt.plot(x1, smoothed1, label="smooth1")
            #plt.plot([i for i in range(0, len(curr_p1[-last_count:]))], curr_p1[-last_count:], label="origin1")
            plt.plot(x2, smoothed2, label="smooth2")
            #plt.plot([i for i in range(0, len(curr_p2[-last_count:]))], curr_p2[-last_count:], label="origin1")
            plt.legend()
            plt.show()
        return results