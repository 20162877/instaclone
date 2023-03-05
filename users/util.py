import pandas as pd
import time
import numpy as np
import datetime
from pathlib import Path


def simulator():
    j = 0
    # Currently hard coding
    data = pd.DataFrame(columns=['user_id', 'timestamp', 'heart_rate', 'respiration_rate', 'Activity'])
    while j < 120:
        user_id = 'abc'
        print(f'Generating Data: ', pd.Timestamp.utcnow())
        # timestamp = (np.datetime64(datetime.datetime.now()).astype('uint64') / 1e6).astype('uint32')
        timestamp = pd.Timestamp.utcnow()
        heart_rate = np.random.randint(20, high=120, dtype=int)
        resp_rate = np.random.randint(10, high=60, dtype=int)
        activity = np.random.randint(2, high=20, dtype=int)
        # print(time.ctime())
        time.sleep(1)
        j += 1
        i = len(data) + 1
        data.loc[i] = [user_id, timestamp, heart_rate, resp_rate, activity]
    data.to_csv('patients.csv')
    print('Generated CSV file')


def readFile(interval):
    print(f'Reading CSv file {Path(__file__).resolve().parent.parent}/patients.csv ')
    data = pd.read_csv(f'{Path(__file__).resolve().parent.parent}/patients.csv')
    data = data.set_index(['timestamp'])
    data.index = pd.to_datetime(data.index)
    intervals = {15: '15min', 30: '30min', 60: '60min'}
    segment = data.resample(intervals[interval], origin='epoch') \
        .agg({'heart_rate': ['mean', 'max'],
              'respiration_rate': ['min', 'mean']})
    new_segment = [segment[i].tolist() for i in segment.columns]
    # for single user
    final_seg = pd.DataFrame(
        {'avg_hr': new_segment[0], 'max_hr': new_segment[1], 'min_rr': new_segment[2], 'avg_rr': new_segment[3]},
        index=segment.index)
    final_seg.reset_index(inplace=True)
    d = {i: final_seg[i].tolist() for i in final_seg.columns}
    qs = [{"USER_ID": 'abc', "TIMESTAMP": d['timestamp'][i],
           'AVG_HR': d['avg_hr'][i], 'MAX_HR': d['max_hr'][i],
           'MIN_RR': d['min_rr'][i], 'AVG_RR': d['avg_rr'][i]} \
          for i in range(final_seg.shape[0])]
    return qs