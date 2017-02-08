#!/usr/bin/env python

import random
from datetime import date, timedelta

NUM_SIMULATIONS = 10000   # Number of Monte Carlo simulations
SAMPLE_CEILING = 60       # A given simulation will be cut off after reaching this value

TODAYS_ISSUE_COUNT = 146

# Stats for past couple of weeks
# daily_progress = [3, -10, 0, 1, -8, -5, -8, -32, -9, -1, -5, -14, -10, -3, 2, -12, 0, 0, 0, 0, 1, -3, 1, 1, 0, 6, 3, 14, 3, -18, -1, -15, -33, -6, -11]  # 5 weeks (3.1 high/med)
# daily_progress = [3, -10, 0, 1, -8, -5, -8, -32, -9, -1, -5, -14, -10, -3, 2, -12, 0, 0, 0, 0, 1]  # 3 weeks (3.1 high/med)
daily_progress = [3, -10, 0, 1, -8, -5, -8, -32, -9, -1, -5, -14, -10, -3]  # 2 weeks (3.1 high/med)

# Run monte carlo simulation
distribution = list()
for i in range(SAMPLE_CEILING):
    distribution.append(0)

for i in range(NUM_SIMULATIONS):
    issues_left = TODAYS_ISSUE_COUNT
    time_spent = 0
    while issues_left > 0 and time_spent < SAMPLE_CEILING:
        issues_left += daily_progress[random.randint(0, len(daily_progress) - 1)]
        time_spent += 1
    distribution[time_spent - 1] += 1

current_day = date.today()
day = timedelta(days=1)

print "Distribution:"
for i in range(SAMPLE_CEILING):
    print("{0:%b %d} - {1}".format(current_day, 100.0 * distribution[i] / NUM_SIMULATIONS))
    current_day += day

print "\nCumulative:"
current_day = date.today()
total = 0
for i in range(SAMPLE_CEILING):
    total += 100.0 * distribution[i] / NUM_SIMULATIONS
    print("{0:%b %d} - {1}".format(current_day, total))
    current_day += day
