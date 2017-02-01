#!/usr/bin/env python

from stat_collector import Stat_Collector
from stat_grapher import Stat_Grapher

# Git credentials
git_user = ''
git_password = ''

# Plotly credentials
plotly_user = ''
plotly_api_key = ''


# Get stats
print "[Collecting stats]"
stats = Stat_Collector(git_user, git_password).get_issues_by_priority(dummy_data=False)
print ""

# Devel Issues by Priority
print "[Graphing Devel Issues by Priority]"
stream_ids = []  # Removed 3 ids
table_title = 'Tower 3.1: Devel Issues by Priority'
table_filename = 'tower_devel_issues_by_priority'
Stat_Grapher(plotly_user, plotly_api_key, stream_ids).graph_issues_by_priority(stats['devel'], build_table=False, table_title=table_title, table_filename=table_filename)


# Testing Issues by Priority
print "[Graphing Testing Issues by Priority]"
stream_ids = []  # Removed 3 ids
table_title = 'Tower 3.1: Test Issues by Priority'
table_filename = 'tower_test_issues_by_priority'
Stat_Grapher(plotly_user, plotly_api_key, stream_ids).graph_issues_by_priority(stats['test'], build_table=False, table_title=table_title, table_filename=table_filename)
