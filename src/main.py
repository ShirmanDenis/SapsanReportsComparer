import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd
import json
import statistics as st
from sapsan_results import SapsanResult, draw, Mode
from reports_comparer import ReportsComparer
from scipy.stats import ttest_ind, mannwhitneyu, ks_2samp
from scipy.interpolate import interp1d
from datetime import datetime
import calendar
import math

# cpu_usage1 = [point['Data'] for point in json_data1['View']['Metrics']['TargetAppSysMetrics'][0]['Graphs'][0]['Points']]
# cpu_usage2 = [point['Data'] for point in json_data2['View']['Metrics']['TargetAppSysMetrics'][0]['Graphs'][0]['Points']]
#session1 = SapsanResult("keweb_Release_1607328508000", 1)
#session2 = SapsanResult("keweb_Release_1607140961000", 1)
session1 = SapsanResult("../resources/YT_Test1", 1, Mode.File)
session2 = SapsanResult("../resources/YT_Test2", 1, Mode.File)

comp = ReportsComparer(session1, session2)

r = comp.compare_percentiles()
draw(session1, session2)