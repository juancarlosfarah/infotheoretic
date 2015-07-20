__author__ = 'juancarlosfarah'

import pymongo
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spi
from copy import deepcopy


class DataPlotter:

    def __init__(self, database=None):
        if database is not None:
            self.db = self.connect(database)
        else:
            self.db = database

        self.colors = ["orange", "red", "blue", "green", "purple",
                       "yellow", "brown", "pink", "magenta", "black"]

    def connect(self, database):
        host = "localhost"
        port = 27017
        mc = pymongo.MongoClient(host=host, port=port)
        return mc.get_database(database)

    def plot_one(self, threshold):

        cursor = self.db.oscillator_simulation.find({"threshold": threshold})

        beta = []
        global_sync = []
        integrated_information = []

        for doc in cursor:
            beta.append(doc['beta'])
            global_sync.append(doc['global_sync'])
            integrated_information.append(doc['integrated_information_e'])

        fig = plt.figure()
        plt.scatter(global_sync, integrated_information)
        plt.xlabel("Global Synchrony")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Global Synchrony\n" +
                  "Threshold = " + str(threshold))
        plt.show(fig)

        fig = plt.figure()
        plt.scatter(beta, integrated_information)
        plt.xlabel("Beta")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Beta\n" +
                  "Threshold = " + str(threshold))
        plt.show(fig)

        return

    def plot(self,
             phi="phi_e",
             save=False,
             path="$HOME",
             ext="svg",
             query=None,
             thresholds=None):

        duration = "Various"

        if not query:
            query = dict()

        if "duration" in query:
            duration = query['duration']

        cursors = dict()
        colors = dict()
        available_colors = ["orange", "red", "blue", "green", "purple",
                            "yellow", "brown", "pink", "magenta", "black"]
        count = 0

        for threshold in thresholds:
            q = deepcopy(query)
            q['threshold'] = threshold
            cursors[threshold] = self.db.oscillator_simulation.find(q)
            colors[threshold] = available_colors[count]
            count += 1

        beta = dict()
        global_sync = dict()
        phi_e_tilde = dict()
        coalition_entropy = dict()
        chi = dict()
        lamda = dict()
        phi_e = dict()

        for key in cursors:
            beta[key] = []
            global_sync[key] = []
            chi[key] = []
            lamda[key] = []
            coalition_entropy[key] = []
            phi_e_tilde[key] = []
            phi_e[key] = []

            for doc in cursors[key]:
                beta[key].append(doc['beta'])
                global_sync[key].append(doc['global_sync'])
                lamda[key].append(doc['lambda'])
                chi[key].append(doc['chi'])
                coalition_entropy[key].append(doc['coalition_entropy'])
                phi_e_tilde[key].append(doc['phi_e_tilde'])
                phi_e[key].append(doc['phi_e'])

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Global Synchrony")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical vs Global Synchrony\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(global_sync[key],
                                       phi_e[key],
                                       color=colors[key],
                                       label=key))
            avg_phi_e = np.average(phi_e[key])
            print "Average Phi E at " + str(key) + " threshold is " + str(avg_phi_e)
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "1." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Beta")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical vs Beta\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta[key],
                                       phi_e[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "2." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Beta")
            plt.ylabel("Chi")
            plt.title("Chi vs Beta\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta[key],
                                       chi[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "3." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Beta")
            plt.ylabel("Lambda")
            plt.title("Lambda vs Beta\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta[key],
                                       lamda[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "4." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Chi")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical vs Chi\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(chi[key],
                                       phi_e[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "5." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Lambda")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical vs Lambda\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(lamda[key],
                                       phi_e[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "6." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Beta")
            plt.ylabel("Coalition Entropy")
            plt.title("Coalition Entropy vs Beta\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta[key],
                                       coalition_entropy[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "7." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Coalition Entropy")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical vs Coalition Entropy\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(coalition_entropy[key],
                                       phi_e[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "8." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Integrated Information Empirical Tilde")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical vs "
                      "Integrated Information Empirical Tilde\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(phi_e_tilde[key],
                                       phi_e[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "9." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        values = []
        for key in cursors:
            labels.append(str(key))
            values.append(phi_e[key])

        plt.xlabel("Integrated Information Empirical")
        plt.ylabel("Frequency")
        plt.title("Integrated Information Empirical\n"
                  "Duration = " + str(duration) + ", Tau = 1")

        handles.append(plt.hist(values, label=labels, bins=50))
        plt.legend(title="Threshold")

        if save:
            fig.savefig(path + "10." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        values = []
        for key in cursors:
            labels.append(str(key))
            values.append(coalition_entropy[key])

        plt.xlabel("Coalition Entropy")
        plt.ylabel("Frequency")
        plt.title("Coalition Entropy\n"
                  "Duration = " + str(duration) + ", Tau = 1")

        handles.append(plt.hist(values, label=labels, bins=50))
        plt.legend(title="Threshold")

        if save:
            fig.savefig(path + "hc-frequency." + ext)
        else:
            plt.show(fig)

        plt.close()

        return

    def plot_curves(self):

        cursors = {
            "0.9": self.db.oscillator_simulation.find({"threshold": 0.9}),
            "0.8": self.db.oscillator_simulation.find({"threshold": 0.8}),
            "0.7": self.db.oscillator_simulation.find({"threshold": 0.7}),
            "0.6": self.db.oscillator_simulation.find({"threshold": 0.6}),
            "0.5": self.db.oscillator_simulation.find({"threshold": 0.5})
        }

        beta = dict()
        global_sync = dict()
        integrated_information = dict()
        chi = dict()
        lamda = dict()

        colors = {
            "0.9": "orange",
            "0.8": "red",
            "0.7": "blue",
            "0.6": "green",
            "0.5": "purple"
        }

        for key in cursors:
            beta[key] = []
            global_sync[key] = []
            chi[key] = []
            lamda[key] = []
            integrated_information[key] = []
            for doc in cursors[key]:
                beta[key].append(doc['beta'])
                global_sync[key].append(doc['global_sync'])
                lamda[key].append(doc['lambda'])
                chi[key].append(doc['chi'])
                integrated_information[key].append(doc['integrated_information_e'])

        fig2 = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Beta")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical over Beta")
            x = beta[key]
            y = integrated_information[key]

            # Combine lists into list of tuples.
            points = zip(x, y)

            # Sort list of tuples by x-value.
            points = sorted(points, key=lambda point: point[0])

            # Split list of tuples into two list of x values any y values.
            x, y = zip(*points)

            # Plot original points.
            plt.plot(x, y, 'ro', color=colors[key], label=key)

            x_new = np.linspace(min(x), max(x), 200)
            spline = spi.InterpolatedUnivariateSpline(x, y)
            spline.set_smoothing_factor(0.15)

            handles.append(plt.plot(x_new,
                                    spline(x_new),
                                    color=colors[key],
                                    label=key))
        plt.ylim(-0.5, 1)
        plt.legend(handles, labels, title="Threshold")
        plt.show(fig2)

        fig3 = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Chi")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical over Chi")
            x = chi[key]
            y = integrated_information[key]

            # Combine lists into list of tuples.
            points = zip(x, y)

            # Sort list of tuples by x-value.
            points = sorted(points, key=lambda point: point[0])

            # Split list of tuples into two list of x values any y values.
            x, y = zip(*points)

            # Plot original points.
            plt.plot(x, y, 'ro', color=colors[key], label=key)

            x_new = np.linspace(min(x), max(x), 200)
            spline = spi.InterpolatedUnivariateSpline(x, y)
            spline.set_smoothing_factor(1.1)

            handles.append(plt.plot(x_new,
                                    spline(x_new),
                                    color=colors[key],
                                    label=key))
        plt.ylim(-0.5, 1)
        plt.legend(handles, labels, title="Threshold")
        plt.show(fig3)

        fig4 = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Lambda")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical over Lambda")
            x = lamda[key]
            y = integrated_information[key]

            # Combine lists into list of tuples.
            points = zip(x, y)

            # Sort list of tuples by x-value.
            points = sorted(points, key=lambda point: point[0])

            # Split list of tuples into two list of x values any y values.
            x, y = zip(*points)

            # Plot original points.
            plt.plot(x, y, 'ro', color=colors[key], label=key)

            x_new = np.linspace(min(x), max(x), 200)
            spline = spi.InterpolatedUnivariateSpline(x, y)
            spline.set_smoothing_factor(1.1)

            handles.append(plt.plot(x_new,
                                    spline(x_new),
                                    color=colors[key],
                                    label=key))
        plt.ylim(-0.5, 1)
        plt.legend(handles, labels, title="Threshold")
        plt.show(fig4)

        fig5 = plt.figure()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            plt.xlabel("Global Synchrony")
            plt.ylabel("Integrated Information Empirical")
            plt.title("Integrated Information Empirical over Global Synchrony")
            x = global_sync[key]
            y = integrated_information[key]

            # Combine lists into list of tuples.
            points = zip(x, y)

            # Sort list of tuples by x-value.
            points = sorted(points, key=lambda point: point[0])

            # Split list of tuples into two list of x values any y values.
            x, y = zip(*points)

            # Plot original points.
            plt.plot(x, y, 'ro', color=colors[key], label=key)

            x_new = np.linspace(min(x), max(x), 200)
            spline = spi.InterpolatedUnivariateSpline(x, y)
            spline.set_smoothing_factor(0.2)

            handles.append(plt.plot(x_new,
                                    spline(x_new),
                                    color=colors[key],
                                    label=key))
        plt.ylim(-0.5, 1)
        plt.legend(handles, labels, title="Threshold")
        plt.show(fig5)

        return

    def plot_surrogate_correlation(self,
                                   phi="integrated_information_e",
                                   save=False,
                                   path="$HOME",
                                   ext="svg",
                                   query=None,
                                   surrogate_type='is_sorted'):

        duration = "Various"

        if not query:
            query = dict()

        if "duration" in query:
            duration = query['duration']

        q1a = deepcopy(query)
        q1b = deepcopy(query)
        q1a['threshold'] = 0.9
        q1a['is_surrogate'] = False
        q1b['threshold'] = 0.9
        q1b[surrogate_type] = True

        q2a = deepcopy(query)
        q2b = deepcopy(query)
        q2a['threshold'] = 0.8
        q2a['is_surrogate'] = False
        q2b['threshold'] = 0.8
        q2b[surrogate_type] = True

        q3a = deepcopy(query)
        q3b = deepcopy(query)
        q3a['threshold'] = 0.7
        q3a['is_surrogate'] = False
        q3b['threshold'] = 0.7
        q3b[surrogate_type] = True

        q4a = deepcopy(query)
        q4b = deepcopy(query)
        q4a['threshold'] = 0.6
        q4a['is_surrogate'] = False
        q4b['threshold'] = 0.6
        q4b[surrogate_type] = True

        q5a = deepcopy(query)
        q5b = deepcopy(query)
        q5a['threshold'] = 0.5
        q5a['is_surrogate'] = False
        q5b['threshold'] = 0.5
        q5b[surrogate_type] = True

        cursors_a = {
            "0.9": self.db.oscillator_simulation.find(q1a).sort('source',
                                                            direction=1),
            "0.8": self.db.oscillator_simulation.find(q2a).sort('source', direction=1),
            "0.7": self.db.oscillator_simulation.find(q3a).sort('source', direction=1),
            "0.6": self.db.oscillator_simulation.find(q4a).sort('source', direction=1),
            "0.5": self.db.oscillator_simulation.find(q5a).sort('source', direction=1)
        }

        cursors_b = {
            "0.9": self.db.oscillator_simulation.find(q1b).sort('source', direction=1),
            "0.8": self.db.oscillator_simulation.find(q2b).sort('source', direction=1),
            "0.7": self.db.oscillator_simulation.find(q3b).sort('source', direction=1),
            "0.6": self.db.oscillator_simulation.find(q4b).sort('source', direction=1),
            "0.5": self.db.oscillator_simulation.find(q5b).sort('source', direction=1)
        }

        beta = {'original': dict(), 'surrogate': dict()}
        global_sync = {'original': dict(), 'surrogate': dict()}
        phi_e = {'original': dict(), 'surrogate': dict()}
        phi_e_tilde = {'original': dict(), 'surrogate': dict()}
        coalition_entropy = {'original': dict(), 'surrogate': dict()}
        chi = {'original': dict(), 'surrogate': dict()}
        lamda = {'original': dict(), 'surrogate': dict()}

        colors = {
            "0.9": "orange",
            "0.8": "red",
            "0.7": "blue",
            "0.6": "green",
            "0.5": "purple"
        }

        for key in cursors_a:
            beta['original'][key] = []
            global_sync['original'][key] = []
            chi['original'][key] = []
            lamda['original'][key] = []
            phi_e['original'][key] = []
            coalition_entropy['original'][key] = []
            phi_e_tilde['original'][key] = []
            for doc in cursors_a[key]:
                beta['original'][key].append(doc['beta'])
                global_sync['original'][key].append(doc['global_sync'])
                lamda['original'][key].append(doc['lambda'])
                chi['original'][key].append(doc['chi'])
                phi_e['original'][key].append(doc[phi])
                coalition_entropy['original'][key].append(doc['coalition_entropy'])
                phi_e_tilde['original'][key].append(doc['phi_e_tilde'])

        for key in cursors_b:
            beta['surrogate'][key] = []
            global_sync['surrogate'][key] = []
            chi['surrogate'][key] = []
            lamda['surrogate'][key] = []
            phi_e['surrogate'][key] = []
            coalition_entropy['surrogate'][key] = []
            phi_e_tilde['surrogate'][key] = []
            for doc in cursors_b[key]:
                beta['surrogate'][key].append(doc['beta'])
                global_sync['surrogate'][key].append(doc['global_sync'])
                lamda['surrogate'][key].append(doc['lambda'])
                chi['surrogate'][key].append(doc['chi'])
                phi_e['surrogate'][key].append(doc[phi])
                coalition_entropy['surrogate'][key].append(doc['coalition_entropy'])
                phi_e_tilde['surrogate'][key].append(doc['phi_e_tilde'])

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Coalition Entropy")
            plt.ylabel("Coalition Entropy Surrogate")
            plt.title("Coalition Entropy Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(coalition_entropy['original'][key],
                                       coalition_entropy['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "coalition_entropy_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Integrated Information")
            plt.ylabel("Integrated Information Surrogate")
            plt.title("Integrated Information Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(phi_e['original'][key],
                                       phi_e['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "phi_e_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Chi")
            plt.ylabel("Chi Surrogate")
            plt.title("Chi Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(chi['original'][key],
                                       chi['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "chi_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Lambda")
            plt.ylabel("Lambda Surrogate")
            plt.title("Lambda Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(lamda['original'][key],
                                       lamda['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "lambda_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Global Synchrony")
            plt.ylabel("Global Synchrony Surrogate")
            plt.title("Global Synchrony Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(global_sync['original'][key],
                                       global_sync['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "global_sync_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Integrated Information Empirical Tilde")
            plt.ylabel("Integrated Information Empirical Tilde Surrogate")
            plt.title("Integrated Information Empirical "
                      "Tilde Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(phi_e_tilde['original'][key],
                                       phi_e_tilde['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "phi_e_tilde_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Beta")
            plt.ylabel("Beta Surrogate")
            plt.title("Beta Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta['original'][key],
                                       beta['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "beta_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Beta Surrogate")
            plt.ylabel("Phi E")
            plt.title("Phi E vs Beta Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta['surrogate'][key],
                                       phi_e['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "phi_e_beta_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Phi E Tilde")
            plt.ylabel("Beta Surrogate")
            plt.title("Phi E Tilde vs Beta Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta['surrogate'][key],
                                       phi_e_tilde['surrogate'][key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "phi_e_tilde_beta_surrogate_analysis." + ext)
        else:
            plt.show(fig)

        return

    def plot_sorted_correlation(self,
                                phi="integrated_information_e",
                                save=False,
                                path="$HOME",
                                ext="svg",
                                query=None):

        duration = "Various"

        if not query:
            query = dict()

        if "duration" in query:
            duration = query['duration']

        q1 = deepcopy(query)
        q1['threshold'] = 0.9

        q2 = deepcopy(query)
        q2['threshold'] = 0.8

        q3 = deepcopy(query)
        q3['threshold'] = 0.7

        q4 = deepcopy(query)
        q4['threshold'] = 0.6

        q5 = deepcopy(query)
        q5['threshold'] = 0.5

        cursors = {
            "0.9": self.db.oscillator_simulation.find(q1),
            "0.8": self.db.oscillator_simulation.find(q2),
            "0.7": self.db.oscillator_simulation.find(q3),
            "0.6": self.db.oscillator_simulation.find(q4),
            "0.5": self.db.oscillator_simulation.find(q5)
        }

        ii = dict()
        ii_sorted = dict()

        colors = {
            "0.9": "orange",
            "0.8": "red",
            "0.7": "blue",
            "0.6": "green",
            "0.5": "purple"
        }

        for key in cursors:
            ii[key] = []
            ii_sorted[key] = []
            for doc in cursors[key]:
                ii[key].append(doc[phi])
                ii_sorted[key].append(doc['phi_e_tilde_sorted'])

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)
            plt.xlabel("Integrated Information")
            plt.ylabel("Integrated Information Sorted")
            plt.title("Integrated Information Sorted Surrogate Data Analysis\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(ii[key],
                                       ii_sorted[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Threshold")

        if save:
            fig.savefig(path + "sorted_surrogate_analysis." + ext)
        else:
            plt.show(fig)


    def plot_mi_analysis(self,
                         save=False,
                         path="$HOME",
                         ext="svg",
                         query=None,
                         duration=5000,
                         num_oscillators=8):

        if not query:
            query = dict()

        if "duration" in query:
            duration = query['duration']
        else:
            query['duration'] = duration

        if "num_oscillators" in query:
            num_oscillators = query['num_oscillators']
        else:
            query['num_oscillators'] = num_oscillators

        cursors = dict()
        colors = dict()
        types = ['sorted', 'shuffled', 'normal']
        available_colors = ["orange", "red", "blue", "green", "purple",
                            "yellow", "brown", "pink", "magenta", "black"]
        count = 0

        for t in types:
            q = deepcopy(query)
            if t == 'sorted':
                q['is_sorted'] = True
            if t == 'shuffled':
                q['is_shuffled'] = True
            if t == 'normal':
                q['is_surrogate'] = False

            cursors[t] = self.db.oscillator_simulation.find(q).sort('source',
                                                                    direction=1)
            colors[t] = available_colors[count]
            count += 1

        beta = dict()
        mi = dict()
        hc = dict()

        for key in cursors:
            beta[key] = []
            mi[key] = []
            hc[key] = []

            for doc in cursors[key]:
                beta[key].append(doc['beta'])
                mi[key].append(doc['mi'])
                hc[key].append(doc['coalition_entropy'])

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)

            plt.xlabel("Beta")
            plt.ylabel("Mutual Information")
            plt.title("Mutual Information vs Beta\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(beta[key],
                                       mi[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Type")

        if save:
            fig.savefig(path + "mi_vs_beta." + ext)
        else:
            plt.show(fig)

        fig = plt.figure()
        handles = []
        labels = []
        for key in colors:
            labels.append(key)

            plt.xlabel("Coalition Entropy")
            plt.ylabel("Mutual Information")
            plt.title("Mutual Information vs Coalition Entropy\n"
                      "Duration = " + str(duration) + ", Tau = 1")
            handles.append(plt.scatter(hc[key],
                                       mi[key],
                                       color=colors[key],
                                       label=key))
        plt.legend(handles, labels, title="Type")

        if save:
            fig.savefig(path + "mi_vs_hc." + ext)
        else:
            plt.show(fig)

        return

    def plot_mi_results(self,
                        save=False,
                        path="$HOME",
                        ext="svg",
                        query=None,
                        duration=5000,
                        num_oscillators=8):

        if query is None:
            query = dict()

        if "duration" in query:
            duration = query['duration']
        else:
            query['duration'] = duration

        if "num_oscillators" in query:
            num_oscillators = query['num_oscillators']
        else:
            query['num_oscillators'] = num_oscillators

        colors = dict()
        types = ['shuffled', 'normal']
        available_colors = ["orange", "red", "blue", "green", "purple",
                            "yellow", "brown", "pink", "magenta", "black"]
        count = 0

        for t in types:
            colors[t] = available_colors[count]
            count += 1

        cursor = self.db.oscillator_simulation.find(query)

        beta = []
        hc = []
        mi = []
        mi_shuffled = []

        for doc in cursor:
            beta.append(doc['beta'])
            mi.append(doc['mi'])
            hc.append(doc['coalition_entropy'])
            mi_shuffled.append(doc['shuffled']['mi'])

        fig = plt.figure()
        handles = []
        labels = ["Normal", "Shuffled"]

        plt.xlabel("Beta")
        plt.ylabel("Mutual Information")
        plt.title("Mutual Information vs Beta\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(beta,
                                   mi,
                                   color=colors['normal'],
                                   label="Normal"))

        handles.append(plt.scatter(beta,
                                   mi_shuffled,
                                   color=colors['shuffled'],
                                   label="Shuffled"))

        plt.legend(handles, labels, title="Type")

        if save:
            fig.savefig(path + "mi_vs_beta." + ext)
        else:
            plt.show(fig)

        # Coalition Entropy
        fig = plt.figure()
        handles = []
        labels = ["Normal", "Shuffled"]
        plt.xlabel("Coalition Entropy")
        plt.ylabel("Mutual Information")
        plt.title("Mutual Information vs Coalition Entropy\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        handles.append(plt.scatter(hc,
                                   mi,
                                   color=colors['normal'],
                                   label="Normal"))
        labels.append("Shuffled")
        handles.append(plt.scatter(hc,
                                   mi_shuffled,
                                   color=colors['shuffled'],
                                   label="Shuffled"))

        plt.legend(handles, labels, title="Type")

        if save:
            fig.savefig(path + "mi_vs_hc." + ext)
        else:
            plt.show(fig)

        # Mutual Information normal vs shuffled.
        fig = plt.figure()
        plt.xlabel("Mutual Information")
        plt.ylabel("Mutual Information Shuffled")
        plt.title("Mutual Information\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        plt.scatter(mi, mi_shuffled)

        if save:
            fig.savefig(path + "mi_vs_mi_shuffled." + ext)
        else:
            plt.show(fig)

        # Difference in Mutual Information vs Hc.
        fig = plt.figure()
        plt.xlabel("Difference in Mutual Information")
        plt.ylabel("Coalition Entropy")
        plt.title("Mutual Information\n"
                  "Duration = " + str(duration) + ", Tau = 1")
        mi_np = np.array(mi)
        mi_shuffled_np = np.array(mi_shuffled)
        mi_diff = np.absolute(mi_np - mi_shuffled_np)
        plt.scatter(hc, mi_diff)

        if save:
            fig.savefig(path + "mi-mi_shuffled_vs_hc." + ext)
        else:
            plt.show(fig)

    def plot_hc(self):
        pass

    def plot_surrogate_analysis(self,
                                path="/",
                                save=False,
                                ext="png"):

        query = {"pattern": "random"}
        cursor = self.db.generator_simulation.find(query)

        hc = []
        mi = []
        phi = []
        mi_shuffled = []
        hc_shuffled = []
        phi_shuffled = []

        for doc in cursor:
            mi.append(doc['mi'])
            hc.append(doc['h_c'])
            phi.append(doc['phi_e'])
            mi_shuffled.append(doc['shuffled']['mi'])
            hc_shuffled.append(doc['shuffled']['h_c'])
            phi_shuffled.append(doc['shuffled']['phi_e'])

        # Mutual Information Analysis
        fig = plt.figure()
        plt.xlabel("Original")
        plt.ylabel("Shuffled")
        plt.title("Mutual Information Analysis in Random Surrogate Data")
        plt.scatter(mi, mi_shuffled)
        if save:
            fig.savefig(path + "surrogate-random-mi-analysis." + ext)
        else:
            plt.show(fig)

        # Coalition Entropy Analysis
        fig = plt.figure()
        plt.xlabel("Original")
        plt.ylabel("Shuffled")
        plt.title("Coalition Entropy Analysis in Random Surrogate Data")
        plt.scatter(hc, hc_shuffled)
        if save:
            fig.savefig(path + "surrogate-random-hc-analysis." + ext)
        else:
            plt.show(fig)

        # Integrated Information Empirical Analysis
        fig = plt.figure()
        plt.xlabel("Original")
        plt.ylabel("Shuffled")
        plt.title("Integrated Information Analysis in Random Surrogate Data")
        plt.scatter(phi, phi_shuffled)
        if save:
            fig.savefig(path + "surrogate-random-phi_e-analysis." + ext)
        else:
            plt.show(fig)

        query = {"pattern": {"$ne": "random"}}
        cursor = self.db.generator_simulation.find(query)

        hc = np.array([])
        mi = np.array([])
        phi = np.array([])
        mi_shuffled = np.array([])
        hc_shuffled = np.array([])
        phi_shuffled = np.array([])
        pattern_len = []

        for doc in cursor:
            mi = np.append(mi, doc['mi'])
            hc = np.append(hc, doc['h_c'])
            phi = np.append(phi, doc['phi_e'])
            mi_shuffled = np.append(mi_shuffled, doc['shuffled']['mi'])
            hc_shuffled = np.append(hc_shuffled, doc['shuffled']['h_c'])
            phi_shuffled = np.append(phi_shuffled, doc['shuffled']['phi_e'])
            pattern_len.append(len(doc['pattern']))

        mi_diff = mi - mi_shuffled
        hc_diff = hc - hc_shuffled
        phi_diff = phi - phi_shuffled
        print mi_diff, hc_diff, phi_diff
        measures = {
            "Coalition Entropy": hc_diff,
            "Mutual Information": mi_diff,
            "Integrated Information": phi_diff
        }

        fig = plt.figure()
        handles = []
        labels = []
        color = 0
        for key in measures:
            labels.append(key)
            plt.xlabel("Length of Pattern")
            plt.ylabel("Difference between Original and Shuffled Data")
            plt.title("Surrogate Analysis with Repeating Patterns")
            handles.append(plt.scatter(pattern_len,
                                       measures[key],
                                       color=self.colors[color],
                                       label=key))
            color += 1
        plt.legend(handles, labels, title="Measure")

        if save:
            fig.savefig(path + "surrogate-pattern-analysis." + ext)
        else:
            plt.show(fig)

        return

    def plot_normalised_surrogate(self,
                                  path="/",
                                  save=False,
                                  ext="png"):

        query = {"shuffled_normalised": {"$exists": True}}
        cursor = self.db.oscillator_simulation.find(query)

        mi = []
        phi = []
        mi_shuffled = []
        phi_shuffled = []

        for doc in cursor:
            mi.append(doc['mi'])
            phi.append(doc['phi_e'])
            mi_shuffled.append(doc['shuffled_normalised']['mi'])
            phi_shuffled.append(doc['shuffled_normalised']['phi_e'])

        # Mutual Information Analysis
        fig = plt.figure()
        plt.xlabel("Original")
        plt.ylabel("Shuffled")
        plt.title("Mutual Information Analysis in Normalised Surrogate Data")
        plt.scatter(mi, mi_shuffled)
        if save:
            fig.savefig(path + "surrogate-normalised-mi-analysis." + ext)
        else:
            plt.show(fig)

        # Phi Analysis
        fig = plt.figure()
        plt.xlabel("Original")
        plt.ylabel("Shuffled")
        plt.title("Integrated Information Analysis in Normalised Surrogate "
                  "Data")
        plt.scatter(mi, mi_shuffled)
        if save:
            fig.savefig(path + "surrogate-normalised-mi-analysis." + ext)
        else:
            plt.show(fig)


if __name__ == "__main__":
    q = {
        'duration': 5000,
        'num_oscillators': 8,
        'is_surrogate': False,
    }
    all_thresholds = [0.9, 0.8, 0.7, 0.6, 0.5]

    dp = DataPlotter(database="infotheoretic")
    # plot_surrogate_correlation(phi="phi_e",
    #                            save=False,
    #                            path="/Users/juancarlosfarah/Git/infotheoretic/docs/surrogate/",
    #                            ext="png")

    # dp.plot(phi='phi_e',
    #         save=False,
    #         path="/Users/juancarlosfarah/Git/infotheoretic/docs/phi_e_tilde/",
    #         ext="svg",
    #         query=q,
    #         thresholds=all_thresholds)

    # plot_mi_results(save=False,
    #                 path="$HOME",
    #                 ext="svg",
    #                 query=q,
    #                 duration=5000,
    #                 num_oscillators=8)

    dp.plot_surrogate_analysis()
    dp.plot_normalised_surrogate()

    # plot_curves()