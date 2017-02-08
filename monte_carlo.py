#!/usr/bin/env python

import random
from datetime import date, timedelta

NUM_SIMULATIONS = 100000   # Number of Monte Carlo simulations
SAMPLE_CEILING = 40       # A given simulation will be cut off after reaching this value

TODAYS_ISSUE_COUNT = 146

# Stats for last two weeks
weekday_progress = [3, -10, -8, -5, -8, -32, -9, -14, -10, -3]
weekend_progress = [0, 1, -1, -5]

# Run monte carlo simulation
distribution = list()
for i in range(SAMPLE_CEILING):
    distribution.append(0)

day = timedelta(days=1)
for i in range(NUM_SIMULATIONS):
    issues_left = TODAYS_ISSUE_COUNT
    time_spent = 0
    current_day = date.today()
    while issues_left > 0 and time_spent < SAMPLE_CEILING:
        if current_day.isoweekday() in range(1, 6):
            issues_left += weekday_progress[random.randint(0, len(weekday_progress) - 1)]
        else:
            issues_left += weekend_progress[random.randint(0, len(weekend_progress) - 1)]
        time_spent += 1
        current_day += day
    distribution[time_spent - 1] += 1

print "Distribution:"
current_day = date.today()
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
