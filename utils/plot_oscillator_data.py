__author__ = 'juancarlosfarah'

import pymongo
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

def connect(database):
    host = "localhost"
    port = 27017
    mc = pymongo.MongoClient(host=host, port=port)
    return mc.get_database(database)


def plot(threshold):
    db = connect("individual_project")

    cursor = db.oscillator_simulation.find({"threshold": threshold})

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

def plot():
    db = connect("individual_project")

    cursors = {
        "0.8": db.oscillator_simulation.find({"threshold": 0.8}),
        "0.7": db.oscillator_simulation.find({"threshold": 0.7}),
        "0.6": db.oscillator_simulation.find({"threshold": 0.6})
    }

    beta = dict()
    global_sync = dict()
    integrated_information = dict()
    colors = {
        "0.8": "red",
        "0.7": "blue",
        "0.6": "green"
    }

    for key in cursors:
        beta[key] = []
        global_sync[key] = []
        integrated_information[key] = []
        for doc in cursors[key]:
            beta[key].append(doc['beta'])
            global_sync[key].append(doc['global_sync'])
            integrated_information[key].append(doc['integrated_information_e'])

    fig1 = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Global Synchrony")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Global Synchrony")
        handles.append(plt.scatter(global_sync[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")
    plt.show(fig1)

    fig2 = plt.figure()
    handles = []
    labels = []
    for key in cursors:
        labels.append(key)
        plt.xlabel("Beta")
        plt.ylabel("Integrated Information Empirical")
        plt.title("Integrated Information Empirical over Beta")
        handles.append(plt.scatter(beta[key],
                                   integrated_information[key],
                                   color=colors[key],
                                   label=key))
    plt.legend(handles, labels, title="Threshold")
    plt.show(fig2)

    return

if __name__ == "__main__":
    plot()