from github import Github
import sys


class Stat_Collector(object):

    def __init__(self, git_user, git_password):
        self.git_user = git_user
        self.git_password = git_password
        self.git_repo = 'ansible/ansible-tower'
        self.milestone_name = 'release_3.1.0'
        self.significant_priority = ['priority:high', 'priority:medium', 'priority:low']

        # Issue labels
        self.component_labels = ['component:api', 'component:ui', 'component:installer',
                                 'component:packaging', 'component:ux', 'component:license_server',
                                 'component:cli']

        self.issue_states = ['state:in_progress', 'state:needs_devel', 'state:needs_docs', 'state:needs_review',
                             'state:needs_test', 'state:test_in_progress']
        self.priority_levels = ['priority:high', 'priority:medium', 'priority:low']
        self.label_groups = {'devel': ['state:in_progress', 'state:needs_devel', 'state:needs_review'],
                             'test': ['state:needs_test', 'state:test_in_progress']}

    def get_issues(self):
        '''Get collection of github issues by milestone'''
        # Connect to git
        print "Connect to git"
        git = Github(self.git_user, self.git_password)
        repo = git.get_repo(self.git_repo)

        # Get milestone
        print "Get milestone"
        milestones = repo.get_milestones(state="open")
        for milestone in milestones:
            if milestone.title == self.milestone_name:
                current_milestone = milestone
                break

        # Collect stats on filters
        print "Collect stats"
        return repo.get_issues(milestone=current_milestone)

    def get_issues_by_component(self, dummy_data=False):
        '''Return mapping of component label to count of high and low severity issues'''
        if dummy_data:
            return {'component:license_server': {'high': 1, 'low': 0},
                    'component:installer':      {'high': 18, 'low': 3},
                    'component:ux':             {'high': 7, 'low': 1},
                    'component:cli':            {'high': 3, 'low': 0},
                    'component:api':            {'high': 73, 'low': 6},
                    'component:ui':             {'high': 167, 'low': 13}}

        # Build empty dictionary for statistics
        open_issues_by_component = dict()
        for label in self.component_labels:                          # FIXME: Dynamically determine labels
            open_issues_by_component[label] = {'high': 0, 'low': 0}  # Note issue count by severity

        issues = self.get_issues()
        total_issue_count = 0

        for issue in issues:

            # Filter out pull requests
            if issue.pull_request:
                # Print progress, ' ' => Skipping Pull Request
                sys.stdout.write(' ')
                sys.stdout.flush()
                continue

            total_issue_count += 1

            # Get label(s)
            labels = issue.get_labels()
            label_list = []
            for label in labels:
                label_list.append(label.name)

            # Determine severity
            # Issues are by default low priority
            significant_issue = False
            for priority in self.significant_priority:
                if priority in label_list:
                    significant_issue = True
                    break

            # Add statistic
            # Issue may be included in tally for multiple components
            for label in label_list:
                if label in self.component_labels:
                    if significant_issue:
                        open_issues_by_component[label]['high'] += 1
                    else:
                        open_issues_by_component[label]['low'] += 1

            # Print progress, '.' => Added new issue
            sys.stdout.write('.')
            sys.stdout.flush()

        print ""
        print "Found %s issues." % total_issue_count
        print "------------------------------------"

        print ""
        print "stats:"
        print open_issues_by_component
        print "------------------------------------"

        return open_issues_by_component

    def get_issues_by_state(self, dummy_data=False):
        '''Return mapping of component state to count of issues'''
        if dummy_data:
            return {'state:needs_docs': 16,
                    'state:needs_test': 122,
                    'state:needs_review': 6,
                    'state:test_in_progress': 18,
                    'state:in_progress': 25,
                    'state:needs_devel': 99}
        # Build empty dictionary for statistics
        issues_by_state = dict()
        for state in self.issue_states:  # FIXME: Dynamically determine states
            issues_by_state[state] = 0

        issues = self.get_issues()
        total_issue_count = 0

        for issue in issues:
            # Filter out pull requests
            if issue.pull_request:
                # Print progress, ' ' => Skipping Pull Request
                sys.stdout.write(' ')
                sys.stdout.flush()
                continue

            total_issue_count += 1

            # Get label(s)
            labels = issue.get_labels()
            label_list = []
            for label in labels:
                label_list.append(label.name)

            # Add statistic
            for label in label_list:
                if label in self.issue_states:
                    issues_by_state[label] += 1

            # Print progress, '.' => Added new issue
            sys.stdout.write('.')
            sys.stdout.flush()

        print ""
        print "Found %s issues." % total_issue_count
        print "------------------------------------"

        print ""
        print "stats:"
        print issues_by_state
        print "------------------------------------"

        return issues_by_state

    def get_issues_by_priority(self, dummy_data=False):
        '''Return mapping of component state to count of issues'''
        if dummy_data:
            return {'test': {'priority:medium': 89,
                             'priority:low': 4,
                             'priority:high': 64},
                    'devel': {'priority:medium': 79,
                              'priority:low': 20,
                              'priority:high': 29}}

        # Build empty dictionary for statistics
        issues_by_severity = dict()
        label_group_names = sorted(self.label_groups.keys())
        for group in label_group_names:
            issues_by_severity[group] = dict()
            for priority in self.priority_levels:
                issues_by_severity[group][priority] = 0

        issues = self.get_issues()
        total_issue_count = 0

        for issue in issues:

            # Filter out pull requests
            if issue.pull_request:
                # Print progress, ' ' => Skipping Pull Request
                sys.stdout.write(' ')
                sys.stdout.flush()

            total_issue_count += 1

            # Get label(s)
            labels = issue.get_labels()
            label_list = []
            for label in labels:
                label_list.append(label.name)

            # Determine label group
            group = None
            for label in label_list:
                for group_name in self.label_groups.keys():
                    if label in self.label_groups[group_name]:
                        group = group_name
                        break
                if group:
                    break
            if not group:
                # Label group not found - skip this issue
                sys.stdout.write('?')
                sys.stdout.flush()
                continue

            # Determine priority, add statistics
            for label in label_list:
                if label in self.priority_levels:
                    priority = label
                    # Add priority
                    issues_by_severity[group][priority] += 1
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    break
            else:
                # Priority not found - skip this issue
                sys.stdout.write('?')
                sys.stdout.flush()
                continue

        print ""
        print "Found %s issues." % total_issue_count
        print "------------------------------------"

        print ""
        print "stats:"
        print issues_by_severity
        print "------------------------------------"

        return issues_by_severity
