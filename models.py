import time
import datetime
import pandas as pd

class Member:
    def __init__(self, name, stars, score, days):
        self.name = " ".join(name.split())
        self.stars = stars
        self.score = score
        self.day_score = []
        #days_df = pd.read_json(days)
        for k, v in days.items():
            if '1' in v and '2' in v:
                self.day_score.append(DailyScore(k, v['1']['get_star_ts'], v['2']['get_star_ts']))
            else:
                self.day_score.append(DailyScore(k, v['1']['get_star_ts'], 0))
        self.day_score.sort(key=lambda h: (h.day))

        if self.day_score and self.day_score[0].pt_b_interval != 0:
            sum = 0
            cnt = 0
            for i in self.day_score:
                if i.pt_b_interval != 0:
                    sum += i.pt_b_interval
                    cnt += 1
            self.average_pt_b = "{:01d}:{:02d}".format(int(sum//cnt), int((sum/cnt - sum//cnt) * 60))

class DailyScore:
    def __init__(self, day, part_a_timestamp, part_b_timestamp):
        self.day = day
        self.pt_a_timestamp = datetime.datetime.fromtimestamp(part_a_timestamp)
        if part_b_timestamp != 0:
            self.pt_b_timestamp = datetime.datetime.fromtimestamp(part_b_timestamp)
            seconds = (self.pt_b_timestamp - self.pt_a_timestamp).total_seconds()
            self.pt_b_interval = seconds / 60
        else:
            self.pt_b_timestamp = 0
            self.pt_b_interval = 0
