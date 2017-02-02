#!/usr/bin/env python

# https://plot.ly/python/
# https://plot.ly/python/multiple-trace-streaming/

import datetime
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go


class Stat_Grapher(object):

    def __init__(self, plotly_user, plotly_api_key, plotly_stream_tokens):
        self.plotly_user = plotly_user
        self.plotly_api_key = plotly_api_key

        # Colors will be mapped to streams in order
        self.colors = ['rgb(195,56,37)',    # Red   (high)
                       'rgb(33,127,188)',   # Blue  (medium)
                       'rgb(26,175,93)',    # Green (low)
                       'rgb(143,63,176)',   # Purple
                       'rgb(246,158,0))',   # Orange
                       'rgb(43,61,81)',     # Navy Blue
                       'rgb(214,84,0)']     # Pumpkin

        self.component_tag = 'component:'  # Component prefix (will be stripped on graph legend)
        self.state_tag = 'state:'          # State prefix (will be stripped on graph legend)
        self.priority_tag = 'priority:'          # State prefix (will be stripped on graph legend)

        # Prepare stream ids
        tls.set_credentials_file(username=self.plotly_user, api_key=self.plotly_api_key, stream_ids=plotly_stream_tokens)
        self.stream_tokens = tls.get_credentials_file()['stream_ids']

    def graph_issues_by_component(self, stats, table_title='Tower 3.1: Issues by Component', table_filename='tower_issues_by_component',
                                  maxpoints=60, build_table=False):  # 60 days
        # Confirm there are enough stream ids
        print "Confirm have enough stream ids"
        components = sorted(stats.keys())
        num_components = len(components)
        assert len(self.stream_tokens) >= num_components, \
            "Not enough plotly stream keys to plot data. Found %s (needed %s)" % \
            (len(self.stream_tokens), num_components)

        stream_ids = []
        for index in range(num_components):
            stream = go.Stream(token=self.stream_tokens[index], maxpoints=maxpoints)
            stream_ids.append(stream)

        # Build Table
        if build_table:
            print "Building plot"
            traces = []
            for index in range(num_components):
                name = components[index].replace(self.component_tag, '')     # Strip component prefix
                trace = go.Scatter(x=[], y=[], stream=stream_ids[index], name=name,
                                   marker=dict(color=self.colors[index]))    # mode='lines+markers'
                traces.append(trace)
            layout = go.Layout(title=table_title)
            fig = go.Figure(data=traces, layout=layout)

            url = py.plot(fig, filename=table_filename)
            print "Graph url: ", url

        # Create streams
        print "Creating streams"
        streams = []
        for index in range(num_components):
            stream = py.Stream(stream_id=self.stream_tokens[index])
            streams.append(stream)

        # Open streams
        print "Opening streams"
        for index in range(num_components):
            streams[index].open()

        # Write data
        print "Writing data"
        for index in range(num_components):
            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            component = components[index]
            y = stats[component]
            streams[index].write(dict(x=x, y=y))

        # Close streams
        print "Closing streams"
        for index in range(num_components):
            streams[index].close()

    def graph_issues_by_state(self, stats, table_title='Tower 3.1: Issues by State', table_filename='tower_issues_by_state',
                              maxpoints=60, build_table=False):  # 60 days
        # Confirm there are enough stream ids
        print "Confirm have enough stream ids"
        states = sorted(stats.keys())
        num_states = len(states)
        assert len(self.stream_tokens) >= num_states, \
            "Not enough plotly stream keys to plot data. Found %s (needed %s)" % \
            (len(self.stream_tokens), num_states)

        stream_ids = []
        for index in range(num_states):
            stream = go.Stream(token=self.stream_tokens[index], maxpoints=maxpoints)
            stream_ids.append(stream)

        # Build Table
        if build_table:
            print "Building plot"
            traces = []
            for index in range(num_states):
                name = states[index].replace(self.state_tag, '')             # Strip state prefix
                trace = go.Scatter(x=[], y=[], stream=stream_ids[index], name=name,
                                   marker=dict(color=self.colors[index]))   # mode='lines+markers'
                traces.append(trace)
            layout = go.Layout(title=table_title)
            fig = go.Figure(data=traces, layout=layout)

            url = py.plot(fig, filename=table_filename)
            print "Graph url: ", url

        # Create streams
        print "Creating streams"
        streams = []
        for index in range(num_states):
            stream = py.Stream(stream_id=self.stream_tokens[index])
            streams.append(stream)

        # Open streams
        print "Opening streams"
        for index in range(num_states):
            streams[index].open()

        # Write data
        print "Writing data"
        for index in range(num_states):
            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            state = states[index]
            y = stats[state]
            streams[index].write(dict(x=x, y=y))

        # Close streams
        print "Closing streams"
        for index in range(num_states):
            streams[index].close()

    def graph_issues_by_priority(self, stats, table_title='Tower 3.1: Issues by Severity', table_filename='tower_issues_by_priority',
                                 maxpoints=60, build_table=False):  # 60 days
        # Confirm there are enough stream ids
        print "Confirm have enough stream ids"

        def priority_weight(priority):
            '''Hack to sort keys logically instead of alphabetically'''
            weight = {'priority:high': 0, 'priority:medium': 1, 'priority:low': 2}
            if priority in weight.keys():
                return weight[priority]
            return 0

        priority_levels = sorted(stats.keys(), key=priority_weight)
        num_priority_levels = len(priority_levels)
        assert len(self.stream_tokens) >= num_priority_levels, \
            "Not enough plotly stream keys to plot data. Found %s (needed %s)" % \
            (len(self.stream_tokens), num_priority_levels)

        stream_ids = []
        for index in range(num_priority_levels):
            stream = go.Stream(token=self.stream_tokens[index], maxpoints=maxpoints)
            stream_ids.append(stream)

        # Build Table
        if build_table:
            print "Building plot"
            traces = []
            for index in range(num_priority_levels):
                name = priority_levels[index].replace(self.priority_tag, '')  # Strip priority prefix
                trace = go.Scatter(x=[], y=[], stream=stream_ids[index], name=name,
                                   marker=dict(color=self.colors[index]))     # mode='lines+markers'
                traces.append(trace)
            layout = go.Layout(title=table_title)
            fig = go.Figure(data=traces, layout=layout)

            url = py.plot(fig, filename=table_filename, show_link=False)
            print "Graph url: ", url

        # Create streams
        print "Creating streams"
        streams = []
        for index in range(num_priority_levels):
            stream = py.Stream(stream_id=self.stream_tokens[index])
            streams.append(stream)

        # Open streams
        print "Opening streams"
        for index in range(num_priority_levels):
            streams[index].open()

        # Write data
        print "Writing data"
        for index in range(num_priority_levels):
            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            priority = priority_levels[index]
            y = stats[priority]
            streams[index].write(dict(x=x, y=y))

        # Close streams
        print "Closing streams"
        for index in range(num_priority_levels):
            streams[index].close()
