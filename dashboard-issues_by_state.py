#!/usr/bin/env python

from stat_collector import Stat_Collector
from stat_grapher import Stat_Grapher

# Git credentials
git_user = ''
git_password = ''

# Plotly credentials
plotly_user = ''
plotly_api_key = ''

stream_ids=[]  # Removed 7 ids

print "[Collecting stats]"
stats = Stat_Collector(git_user, git_password).get_issues_by_state(dummy_data=False)
print ""

print "[Graphing stats]"
Stat_Grapher(plotly_user, plotly_api_key, stream_ids).graph_issues_by_state(stats, build_table=False)

