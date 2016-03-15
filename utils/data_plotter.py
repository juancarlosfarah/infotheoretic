__author__ = 'juancarlosfarah'

import pymongo
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spi
import math
from matplotlib import cm
from copy import deepcopy
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D

# Custom sizes for text in plots.
# ===============================
plt.rcParams.update({'axes.labelsize': 'xx-large'})
plt.rcParams.update({'xtick.labelsize': 'x-large'})
plt.rcParams.update({'ytick.labelsize': 'x-large'})
plt.rcParams.update({'axes.titlesize': 'xx-large'})
plt.rcParams.update({'figure.titlesize': 'xx-large'})
plt.rcParams.update({'legend.fontsize': 'x-large'})
plt.rcParams.update({'font.family': 'serif'})
plt.rcParams.update({'xtick.major.pad': 12})
plt.rcParams.update({'ytick.major.pad': 12})


class DataPlotter:

    def __init__(self, community_type, database=None):
        if database is not None:
            self.db = self.connect(database)
        else:
            self.db = database

        self.community_type = community_type
        self.colors = ["orange", "red", "blue", "green", "purple",
                       "yellow", "brown", "pink", "magenta", "black"]

    def connect(self, database):
        host = "localhost"
        port = 27017
        mc = pymongo.MongoClient(host=host, port=port)
        return mc.get_database(database)

    # noinspection PyUnresolvedReferences
    def plot(self,
             save=False,
             path="$HOME",
             ext="svg",
             query=None,
             tau=1,
             gamma=0.5,
             is_sorted=False,
             is_shuffled=False):

        if not query:
            query = dict()

        duration = "Various"
        key = "tau_" + str(tau) + "_gamma_" + str(gamma).split(".")[1]
        query[key] = {"$exists": True}

        if "duration" in query:
            duration = query['duration']

        cursors = dict()
        colors = dict()
        available_colors = ["red"]
        if len(thresholds) == 2:
            available_colors = ["blue", "red"]
        elif len(thresholds) == 3:
            available_colors = ["green", "blue", "red"]
        elif len(thresholds) > 3:
            available_colors = ["orange", "red", "blue", "green", "purple",
                                "yellow", "brown", "pink", "magenta", "black"]
        count = 0

        for threshold in thresholds:
            q = deepcopy(query)
            q['threshold'] = threshold
            cursors[threshold] = self.db[self.community_type + '_simulation'] \
                                     .find(q)
            colors[threshold] = available_colors[count]
            count += 1

        if self.community_type == 'oscillator' or \
           self.community_type == 'kuramoto':
            beta = dict()
            chi = dict()
        elif self.community_type == 'snn':
            weight = dict()
            scp = dict()

        global_sync = dict()
        phi_e_tilde = dict()
        phi_e_tilde_original = dict()
        coalition_entropy = dict()
        hc_original = dict()
        lamda = dict()
        lambda_skew = dict()
        phi_e = dict()
        phi_e_original = dict()
        mi = dict()

        for key in cursors:
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                beta[key] = []
                chi[key] = []
                lambda_skew[key] = []
            elif self.community_type == 'snn':
                weight[key] = []
                scp[key] = []

            global_sync[key] = []
            lamda[key] = []
            coalition_entropy[key] = []
            phi_e_tilde[key] = []
            phi_e[key] = []
            mi[key] = []

            for doc in cursors[key]:
                subdoc = doc[key]
                if is_sorted:
                    subdoc = doc['sorted']
                elif is_shuffled:
                    subdoc = doc['shuffled']

                if self.community_type == 'oscillator' or \
                   self.community_type == 'kuramoto':
                    beta[key].append(doc['beta'])
                    chi[key].append(doc['chi'])
                    lambda_skew[key].append(doc['lambda_skew'])
                elif self.community_type == 'snn':
                    weight[key].append(doc['weight'])
                    scp[key].append(doc['synaptic_connection_probability'])

                global_sync[key].append(doc['global_sync'])
                lamda[key].append(doc['lambda'])

                # Tau and surrogate dependent measures.
                phi_e_tilde[key].append(subdoc['phi_e_tilde'])
                phi_e[key].append(subdoc['phi_e'])
                mi[key].append(subdoc['mi'])

                if is_sorted or is_shuffled:
                    coalition_entropy[key].append(subdoc['coalition_entropy'])
                    mi[key].append(subdoc['mi'])
                else:
                    coalition_entropy[key].append(doc['coalition_entropy'])

        # Plot both Empirical Phi and Empirical Phi Tilde
        run = 0
        for phi in [phi_e, phi_e_tilde]:
            phi_label = r"Empirical Integrated Information ($\Phi_{E}$)"
            # phi_original = phi_e_original
            phi_sorted_label = r"Empirical Integrated Information " \
                               r"Sorted ($\Phi'_{E}$)"
            phi_shuffled_label = r"Empirical Integrated Information " \
                                 r"Shuffled ($\Phi''_{E}$)"
            if run == 1:
                phi_label = r"Empirical Integrated Information Tilde (" \
                            r"$\widetilde{\Phi}_{E}$)"
                # phi_original = phi_e_tilde_original
                phi_sorted_label = r"Empirical Integrated Information Tilde " \
                                   r"Sorted ($\widetilde{\Phi}'_{E}$)"
                phi_shuffled_label = r"Empirical Integrated Information Tilde" \
                                     r" Shuffled ($\widetilde{\Phi}''_{E}$)"

            # Phi vs Global Synchrony
            # -----------------------
            fig = plt.figure()
            handles = []
            labels = []
            for key in cursors:
                labels.append(key)
                plt.xlabel(r"Global Synchrony ($\Psi$)")
                plt.ylabel(phi_label)
                handles.append(plt.scatter(global_sync[key],
                                           phi[key],
                                           color=colors[key],
                                           label=key))
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if tau == 1:
                    if run == 0:
                        plt.ylim(ymin=-0.15, ymax=0.7)
                    else:
                        plt.ylim(ymin=-0.01, ymax=0.8)
                plt.xlim(xmin=0, xmax=1)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.2, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1.2)
                plt.xlim(xmin=0, xmax=0.7)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda x: x[0]))
            legend = plt.legend(handles, labels, loc=2,
                                title=r"Threshold ($\gamma$)")
            plt.setp(legend.get_title(), fontsize='xx-large')

            if save:
                fig.savefig(path + "1." + ext)
            else:
                plt.show(fig)

            # Phi vs Global Synchrony vs Beta
            # -------------------------------
            fig = plt.figure()
            handles = []
            labels = []
            # Only append values for 0.7 gamma.
            key = 0.7
            labels.append(key)
            plt.xlabel(r"Global Synchrony ($\Psi$)")
            plt.ylabel(phi_label)
            p = plt.scatter(global_sync[key],
                            phi[key],
                            c=beta[key],
                            cmap='jet',
                            label=key)
            handles.append(p)
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if tau == 1:
                    if run == 0:
                        plt.ylim(ymin=-0.15, ymax=0.7)
                    else:
                        plt.ylim(ymin=-0.01, ymax=0.8)
                plt.xlim(xmin=0, xmax=1)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.2, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1.2)
                plt.xlim(xmin=0, xmax=0.7)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda x: x[0]))
            legend = plt.legend(handles, labels, loc=2,
                                title=r"Threshold ($\gamma$)")
            plt.setp(legend.get_title(), fontsize='xx-large')
            plt.colorbar(p)

            if save:
                fig.savefig(path + "1." + ext)
            else:
                plt.show(fig)

            # Hc vs Global Synchrony
            # -----------------------
            # fig = plt.figure()
            # handles = []
            # labels = []
            # for key in cursors:
            #     labels.append(key)
            #     plt.xlabel(r"Global Synchrony ($\Psi$)")
            #     plt.ylabel(r"Coalition Entropy ($H_c$)")
            #     handles.append(plt.scatter(global_sync[key],
            #                                coalition_entropy[key],
            #                                color=colors[key],
            #                                label=key))
            #
            # plt.title(r"$\tau$ = " + str(tau))
            # labels, handles = zip(*sorted(zip(labels, handles),
            #                               key=lambda x: x[0]))
            # legend = plt.legend(handles, labels, loc=2,
            #                     title=r"Threshold ($\gamma$)")
            # plt.setp(legend.get_title(), fontsize='xx-large')
            #
            # if save:
            #     fig.savefig(path + "1." + ext)
            # else:
            #     plt.show(fig)

            # Phi vs Lambda
            # -------------
            fig = plt.figure()
            handles = []
            labels = []
            for key in cursors:
                labels.append(key)
                handles.append(plt.scatter(lamda[key],
                                           phi[key],
                                           color=colors[key],
                                           label=key))
            plt.xlabel(r"Metastability Index ($\lambda$)")
            plt.ylabel(phi_label)
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if tau == 1:
                    if run == 0:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.15, ymax=0.6)
                        else:
                            plt.ylim(ymin=-0.15, ymax=0.7)
                    else:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.01, ymax=0.7)
                        else:
                            plt.ylim(ymin=-0.01, ymax=0.8)
                plt.xlim(xmin=0, xmax=0.05)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.4, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1)
                plt.xlim(xmin=0, xmax=0.06)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda x: x[0]))
            legend = plt.legend(handles, labels, loc=2,
                                title=r"Threshold ($\gamma$)")
            plt.setp(legend.get_title(), fontsize='xx-large')
            if save:
                fig.savefig(path + "6." + ext)
            else:
                plt.show(fig)

            # Phi vs Lambda vs Beta
            # ---------------------
            fig = plt.figure()
            handles = []
            labels = []

            # Only append values for 0.7 gamma.
            key = 0.7
            labels.append(key)
            p = plt.scatter(lamda[key],
                            phi[key],
                            c=beta[key],
                            cmap="jet",
                            label=key)
            handles.append(p)
            plt.xlabel(r"Metastability Index ($\lambda$)")
            plt.ylabel(phi_label)
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if tau == 1:
                    if run == 0:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.15, ymax=0.6)
                        else:
                            plt.ylim(ymin=-0.15, ymax=0.7)
                    else:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.01, ymax=0.7)
                        else:
                            plt.ylim(ymin=-0.01, ymax=0.8)
                plt.xlim(xmin=0, xmax=0.05)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.4, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1)
                plt.xlim(xmin=0, xmax=0.06)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda z: z[0]))
            legend = plt.legend(handles, labels, loc=2,
                                title=r"Threshold ($\gamma$)")
            plt.colorbar(p)
            plt.setp(legend.get_title(), fontsize='xx-large')
            if save:
                fig.savefig(path + "6." + ext)
            else:
                plt.show(fig)

            # Phi vs Lambda Skew
            # ------------------
            fig = plt.figure()
            handles = []
            labels = []
            for key in cursors:
                labels.append(key)
                handles.append(plt.scatter(lambda_skew[key],
                                           phi[key],
                                           color=colors[key],
                                           label=key))
            plt.xlabel(r"Metastability Index Skew ($\lambda_s$)")
            plt.ylabel(phi_label)
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if tau == 1:
                    if run == 0:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.15, ymax=0.6)
                        else:
                            plt.ylim(ymin=-0.15, ymax=0.7)
                    else:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.01, ymax=0.7)
                        else:
                            plt.ylim(ymin=-0.01, ymax=0.8)
                plt.xlim(xmin=0, xmax=0.06)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.4, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1)
                plt.xlim(xmin=0, xmax=0.06)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda x: x[0]))
            legend = plt.legend(handles, labels, loc=1,
                                title=r"Threshold ($\gamma$)")
            plt.setp(legend.get_title(), fontsize='xx-large')
            if save:
                fig.savefig(path + "6." + ext)
            else:
                plt.show(fig)

            # Phi vs Lambda Skew vs Beta
            # --------------------------
            fig = plt.figure()
            handles = []
            labels = []

            # Only append values for 0.7 gamma.
            key = 0.7
            labels.append(key)
            p = plt.scatter(lambda_skew[key],
                            phi[key],
                            c=beta[key],
                            cmap="jet",
                            label=key)
            handles.append(p)
            plt.xlabel(r"Metastability Index Skew ($\lambda_s$)")
            plt.ylabel(phi_label)
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if tau == 1:
                    if run == 0:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.15, ymax=0.6)
                        else:
                            plt.ylim(ymin=-0.15, ymax=0.7)
                    else:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.01, ymax=0.7)
                        else:
                            plt.ylim(ymin=-0.01, ymax=0.8)
                plt.xlim(xmin=0, xmax=0.05)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.4, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1)
                plt.xlim(xmin=0, xmax=0.06)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda z: z[0]))
            legend = plt.legend(handles, labels, loc=2,
                                title=r"Threshold ($\gamma$)")
            plt.colorbar(p)
            plt.setp(legend.get_title(), fontsize='xx-large')
            if save:
                fig.savefig(path + "6." + ext)
            else:
                plt.show(fig)

            # Phi vs Coalition Entropy
            # ------------------------
            fig = plt.figure()
            handles = []
            labels = []
            for key in cursors:
                labels.append(key)
                handles.append(plt.scatter(coalition_entropy[key],
                                           phi[key],
                                           color=colors[key],
                                           label=key))
            plt.xlabel(r"Coalition Entropy ($H_C$)")

            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if is_sorted:
                    plt.ylabel(phi_sorted_label)
                elif is_shuffled:
                    plt.ylabel(phi_shuffled_label)
                else:
                    plt.ylabel(phi_label)

                if tau == 1:
                    if run == 0:
                        plt.ylim(ymin=-0.15, ymax=0.7)

                        if is_sorted:
                            plt.ylim(ymin=-0.55, ymax=0.15)
                        if is_shuffled:
                            plt.ylim(ymin=-0.05, ymax=1.8)
                    else:
                        plt.ylim(ymin=-0.01, ymax=0.8)
                        if is_sorted:
                            plt.ylim(ymin=-0.3, ymax=0.15)
                        if is_shuffled:
                            plt.ylim(ymin=-0.05, ymax=1.8)
                plt.xlim(xmin=0, xmax=1)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.5, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1)
                plt.xlim(xmin=0, xmax=2)
                plt.ylabel(phi_label)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda z: z[0]))
            location = 3 if is_sorted else 2
            legend = plt.legend(handles, labels, loc=location,
                                title=r"Threshold ($\gamma$)")
            plt.setp(legend.get_title(), fontsize='xx-large')

            if save:
                fig.savefig(path + "8." + ext)
            else:
                plt.show(fig)

            # Phi vs Coalition Entropy vs Beta
            # --------------------------------
            fig = plt.figure()
            handles = []
            labels = []

            # Only append values for 0.7 gamma.
            key = 0.7
            labels.append(key)
            p = plt.scatter(coalition_entropy[key],
                            phi[key],
                            c=beta[key],
                            cmap='jet',
                            label=key)
            handles.append(p)
            plt.xlabel(r"Coalition Entropy ($H_C$)")

            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':
                if is_sorted:
                    plt.ylabel(phi_sorted_label)
                elif is_shuffled:
                    plt.ylabel(phi_shuffled_label)
                else:
                    plt.ylabel(phi_label)

                if tau == 1:
                    if run == 0:
                        plt.ylim(ymin=-0.15, ymax=0.7)

                        if is_sorted:
                            plt.ylim(ymin=-0.55, ymax=0.15)
                        if is_shuffled:
                            plt.ylim(ymin=-0.05, ymax=1.8)
                    else:
                        plt.ylim(ymin=-0.01, ymax=0.8)
                        if is_sorted:
                            plt.ylim(ymin=-0.3, ymax=0.15)
                        if is_shuffled:
                            plt.ylim(ymin=-0.05, ymax=1.8)
                plt.xlim(xmin=0, xmax=1)
            else:
                if run == 0:
                    plt.ylim(ymin=-2.5, ymax=0.6)
                else:
                    plt.ylim(ymin=0, ymax=1)
                plt.xlim(xmin=0, xmax=2)
                plt.ylabel(phi_label)
                plt.title(r"$\tau$ = " + str(tau))
            labels, handles = zip(*sorted(zip(labels, handles),
                                          key=lambda z: z[0]))
            location = 3 if is_sorted else 2
            legend = plt.legend(handles, labels, loc=location,
                                title=r"Threshold ($\gamma$)")
            plt.setp(legend.get_title(), fontsize='xx-large')
            plt.colorbar(p)

            if save:
                fig.savefig(path + "8." + ext)
            else:
                plt.show(fig)

            # ==============
            # Kuramoto Plots
            # ==============
            if self.community_type == 'oscillator' or \
               self.community_type == 'kuramoto':

                # ---------------------------
                # Measures not involving Phi.
                # ---------------------------

                # Only show them the first time round.
                if run == 0:

                    # Coalition Entropy vs Beta
                    # -------------------------
                    # fig = plt.figure()
                    # handles = []
                    # labels = []
                    # for key in cursors:
                    #     labels.append(key)
                    #     handles.append(plt.scatter(beta[key],
                    #                                coalition_entropy[key],
                    #                                color=colors[key],
                    #                                label=key))
                    # plt.xlabel(r"$\beta$")
                    # plt.ylabel(r"Coalition Entropy ($H_C$)")
                    # if len(thresholds) == 1:
                    #     plt.ylim(ymin=-0.01, ymax=1)
                    # else:
                    #     plt.ylim(ymin=-0.01, ymax=1)
                    #
                    # if 'beta' in query:
                    #     plt.xlim(xmin=0, xmax=0.8)
                    #     plt.xticks([0, np.pi / 16, np.pi / 8,
                    #                 3 * np.pi / 16, np.pi / 4],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{16}$',
                    #                 r'$\frac{\pi}{8}$',
                    #                 r'$\frac{3\pi}{16}$',
                    #                 r'$\frac{\pi}{4}$'])
                    # else:
                    #     plt.xlim(xmin=0, xmax=6.3)
                    #     plt.xticks([0, np.pi / 2, np.pi,
                    #                 3 * np.pi / 2, 2 * np.pi],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{2}$',
                    #                 r'$\pi$',
                    #                 r'$\frac{3\pi}{2}$',
                    #                 r'$2\pi$'])
                    # labels, handles = zip(*sorted(zip(labels, handles),
                    #                               key=lambda x: x[0]))
                    # legend = plt.legend(handles, labels,
                    #                     title=r"Threshold ($\gamma$)")
                    # plt.setp(legend.get_title(), fontsize='xx-large')
                    # if save:
                    #     fig.savefig(path + "7." + ext)
                    # else:
                    #     plt.show(fig)

                    # Global Synchrony vs Beta
                    # ------------------------
                    # fig = plt.figure()
                    # handles = []
                    # labels = []
                    # for key in cursors:
                    #     labels.append(key)
                    #     handles.append(plt.scatter(beta[key],
                    #                                global_sync[key],
                    #                                color=colors[key],
                    #                                label=key))
                    # plt.xlabel(r"$\beta$")
                    # plt.ylabel(r"Global Synchrony ($\Psi$)")
                    # plt.ylim(ymin=0, ymax=1.01)
                    # if 'beta' in query:
                    #     plt.xlim(xmin=0, xmax=0.8)
                    #     plt.xticks([0, np.pi / 16, np.pi / 8,
                    #                 3 * np.pi / 16, np.pi / 4],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{16}$',
                    #                 r'$\frac{\pi}{8}$',
                    #                 r'$\frac{3\pi}{16}$',
                    #                 r'$\frac{\pi}{4}$'])
                    # else:
                    #     plt.xlim(xmin=0, xmax=6.3)
                    #     plt.xticks([0, np.pi / 2, np.pi,
                    #                 3 * np.pi / 2, 2 * np.pi],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{2}$',
                    #                 r'$\pi$',
                    #                 r'$\frac{3\pi}{2}$',
                    #                 r'$2\pi$'])
                    # location = 2 if 'beta' in query else 1
                    # legend = plt.legend(handles, labels, loc=location,
                    #                     title=r"Threshold ($\gamma$)")
                    # plt.setp(legend.get_title(), fontsize='xx-large')
                    #
                    # if save:
                    #     fig.savefig(path + "7." + ext)
                    # else:
                    #     plt.show(fig)

                    # Chimera Index vs Beta
                    # ---------------------
                    # fig = plt.figure()
                    # handles = []
                    # labels = []
                    # for key in cursors:
                    #     labels.append(key)
                    #     handles.append(plt.scatter(beta[key],
                    #                                chi[key],
                    #                                color=colors[key],
                    #                                label=key))
                    # plt.xlabel(r"$\beta$")
                    # plt.ylabel(r"Chimera Index ($\chi$)")
                    # plt.ylim(ymin=-0.001, ymax=0.05)
                    # if 'beta' in query:
                    #     plt.xlim(xmin=0, xmax=0.8)
                    #     plt.xticks([0, np.pi / 16, np.pi / 8,
                    #                 3 * np.pi / 16, np.pi / 4],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{16}$',
                    #                 r'$\frac{\pi}{8}$',
                    #                 r'$\frac{3\pi}{16}$',
                    #                 r'$\frac{\pi}{4}$'])
                    # else:
                    #     plt.xlim(xmin=0, xmax=6.3)
                    #     plt.xticks([0, np.pi / 2, np.pi,
                    #                 3 * np.pi / 2, 2 * np.pi],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{2}$',
                    #                 r'$\pi$',
                    #                 r'$\frac{3\pi}{2}$',
                    #                 r'$2\pi$'])
                    # legend = plt.legend(handles, labels, loc=1,
                    #                     title=r"Threshold ($\gamma$)")
                    # plt.setp(legend.get_title(), fontsize='xx-large')
                    #
                    # if save:
                    #     fig.savefig(path + "3." + ext)
                    # else:
                    #     plt.show(fig)

                    # Lambda vs Beta
                    # --------------
                    # fig = plt.figure()
                    # handles = []
                    # labels = []
                    # for key in cursors:
                    #     labels.append(key)
                    #     handles.append(plt.scatter(beta[key],
                    #                                lamda[key],
                    #                                color=colors[key],
                    #                                label=key))
                    # # plt.title("Lambda vs Beta\nTau = 1")
                    # plt.xlabel(r"$\beta$")
                    # plt.ylabel(r"Metastability Index ($\lambda$)")
                    # plt.ylim(ymin=-0.001, ymax=0.05)
                    # if 'beta' in query:
                    #     plt.xlim(xmin=-0.01, xmax=0.8)
                    #     plt.xticks([0, np.pi / 16, np.pi / 8,
                    #                 3 * np.pi / 16, np.pi / 4],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{16}$',
                    #                 r'$\frac{\pi}{8}$',
                    #                 r'$\frac{3\pi}{16}$',
                    #                 r'$\frac{\pi}{4}$'])
                    # else:
                    #     plt.xlim(xmin=-0.05, xmax=6.3)
                    #     plt.xticks([0, np.pi / 2, np.pi,
                    #                 3 * np.pi / 2, 2 * np.pi],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{2}$',
                    #                 r'$\pi$',
                    #                 r'$\frac{3\pi}{2}$',
                    #                 r'$2\pi$'])
                    # legend = plt.legend(handles, labels, loc=1,
                    #                     title=r"Threshold ($\gamma$)")
                    # plt.setp(legend.get_title(), fontsize='xx-large')
                    #
                    # if save:
                    #     fig.savefig(path + "4." + ext)
                    # else:
                    #     plt.show(fig)

                    # Lambda Skew vs Beta
                    # -------------------
                    # fig = plt.figure()
                    # handles = []
                    # labels = []
                    # for key in cursors:
                    #     labels.append(key)
                    #     handles.append(plt.scatter(beta[key],
                    #                                lambda_skew[key],
                    #                                color=colors[key],
                    #                                label=key))
                    # plt.xlabel(r"$\beta$")
                    # plt.ylabel(r"Metastability Index Skew ($\lambda_{s}$)")
                    # plt.ylim(ymin=-0.001, ymax=0.05)
                    # if 'beta' in query:
                    #     plt.xlim(xmin=-0.01, xmax=0.8)
                    #     plt.xticks([0, np.pi / 16, np.pi / 8,
                    #                 3 * np.pi / 16, np.pi / 4],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{16}$',
                    #                 r'$\frac{\pi}{8}$',
                    #                 r'$\frac{3\pi}{16}$',
                    #                 r'$\frac{\pi}{4}$'])
                    # else:
                    #     plt.xlim(xmin=-0.05, xmax=6.3)
                    #     plt.xticks([0, np.pi / 2, np.pi,
                    #                 3 * np.pi / 2, 2 * np.pi],
                    #                ['$0$',
                    #                 r'$\frac{\pi}{2}$',
                    #                 r'$\pi$',
                    #                 r'$\frac{3\pi}{2}$',
                    #                 r'$2\pi$'])
                    # legend = plt.legend(handles, labels, loc=1,
                    #                     title=r"Threshold ($\gamma$)")
                    # plt.setp(legend.get_title(), fontsize='xx-large')
                    #
                    # if save:
                    #     fig.savefig(path + "4." + ext)
                    # else:
                    #     plt.show(fig)

                    # Allow disabling all plots under this block.
                    pass

                # -----------------------
                # Measures involving Phi.
                # -----------------------

                # Phi vs Beta
                # -----------
                fig = plt.figure()
                handles = []
                labels = []
                for key in cursors:
                    labels.append(key)
                    handles.append(plt.scatter(beta[key],
                                               phi[key],
                                               color=colors[key],
                                               label=key))
                plt.xlabel(r"$\beta$")
                plt.ylabel(phi_label)
                if tau == 1:
                    if run == 0:
                        if len(thresholds) == 1:
                            plt.ylim(ymin=-0.1, ymax=0.51)
                        else:
                            plt.ylim(ymin=-0.15, ymax=0.71)

                        if is_sorted:
                            plt.ylim(ymin=-0.5, ymax=0.1)
                    else:
                        plt.ylim(ymin=-0.01, ymax=0.65)

                        if is_sorted:
                            plt.ylim(ymin=-0.25, ymax=0.1)

                if 'beta' in query:
                    plt.xlim(xmin=-0.01, xmax=0.8)
                    plt.xticks([0, np.pi / 16, np.pi / 8,
                                3 * np.pi / 16, np.pi / 4],
                               ['$0$',
                                r'$\frac{\pi}{16}$',
                                r'$\frac{\pi}{8}$',
                                r'$\frac{3\pi}{16}$',
                                r'$\frac{\pi}{4}$'])
                else:
                    plt.xlim(xmin=-0.05, xmax=6.3)
                    plt.xticks([0, np.pi / 2, np.pi,
                                3 * np.pi / 2, 2 * np.pi],
                               ['$0$',
                                r'$\frac{\pi}{2}$',
                                r'$\pi$',
                                r'$\frac{3\pi}{2}$',
                                r'$2\pi$'])

                labels, handles = zip(*sorted(zip(labels, handles),
                                              key=lambda x: x[0]))
                legend = plt.legend(handles, labels,
                                    title=r"Threshold ($\gamma$)")
                plt.setp(legend.get_title(), fontsize='xx-large')

                if save:
                    fig.savefig(path + "2." + ext)
                else:
                    plt.show(fig)

                # Phi vs Chi
                # ----------
                fig = plt.figure()
                handles = []
                labels = []
                for key in cursors:
                    labels.append(key)
                    plt.xlabel(r"Chimera Index ($\chi$)")
                    plt.ylabel(phi_label)
                    if tau == 1:
                        if run == 0:
                            if len(thresholds) == 3:
                                plt.ylim(ymin=-0.15, ymax=0.6)
                            else:
                                plt.ylim(ymin=-0.15, ymax=0.7)
                        else:
                            if len(thresholds) == 3:
                                plt.ylim(ymin=-0.01, ymax=0.7)
                            else:
                                plt.ylim(ymin=-0.01, ymax=0.8)
                    plt.xlim(xmin=0, xmax=0.05)
                    handles.append(plt.scatter(chi[key],
                                               phi[key],
                                               color=colors[key],
                                               label=key))
                labels, handles = zip(*sorted(zip(labels, handles),
                                              key=lambda z: z[0]))
                legend = plt.legend(handles, labels, loc=2,
                                    title=r"Threshold ($\gamma$)")
                plt.setp(legend.get_title(), fontsize='xx-large')
                if save:
                    fig.savefig(path + "5." + ext)
                else:
                    plt.show(fig)

                # Phi vs Chi vs Beta
                # ------------------
                fig = plt.figure()
                handles = []
                labels = []

                # Only append values for 0.7 gamma.
                key = 0.7
                labels.append(key)
                plt.xlabel(r"Chimera Index ($\chi$)")
                plt.ylabel(phi_label)
                if tau == 1:
                    if run == 0:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.15, ymax=0.6)
                        else:
                            plt.ylim(ymin=-0.15, ymax=0.7)
                    else:
                        if len(thresholds) == 3:
                            plt.ylim(ymin=-0.01, ymax=0.7)
                        else:
                            plt.ylim(ymin=-0.01, ymax=0.8)
                plt.xlim(xmin=0, xmax=0.05)
                p = plt.scatter(chi[key],
                                phi[key],
                                c=beta[key],
                                cmap="jet",
                                label=key)
                handles.append(p)
                labels, handles = zip(*sorted(zip(labels, handles),
                                              key=lambda z: z[0]))
                legend = plt.legend(handles, labels, loc=2,
                                    title=r"Threshold ($\gamma$)")
                plt.setp(legend.get_title(), fontsize='xx-large')
                plt.colorbar(p)
                if save:
                    fig.savefig(path + "5." + ext)
                else:
                    plt.show(fig)

                # Surrogate data plots.
                # =====================
                # if is_sorted or is_shuffled:
                #
                #     # Phi Surrogate vs Phi
                #     # --------------------
                #     fig = plt.figure()
                #     handles = []
                #     labels = []
                #     location = 1
                #     for key in cursors:
                #
                #         # Legend labels.
                #         labels.append(key)
                #
                #         # Axes labels.
                #         plt.xlabel(phi_label)
                #         if is_sorted:
                #             plt.ylabel(phi_sorted_label)
                #         elif is_shuffled:
                #             plt.ylabel(phi_shuffled_label)
                #
                #         # Axes ranges.
                #         if run == 0:
                #             plt.xlim(xmin=-0.15, xmax=0.7)
                #             if is_sorted:
                #                 plt.ylim(ymin=-0.5, ymax=0.1)
                #             if is_shuffled:
                #                 plt.ylim(ymin=-0.05, ymax=1.8)
                #                 location = 2
                #         else:
                #             plt.xlim(xmin=-0.01, xmax=0.8)
                #             if is_sorted:
                #                 plt.ylim(ymin=-0.25, ymax=0.1)
                #             if is_shuffled:
                #                 plt.ylim(ymin=-0.05, ymax=1.8)
                #                 location = 2
                #
                #         # Plot and assign to handles for legend.
                #         handles.append(plt.scatter(phi_original[key],
                #                                    phi[key],
                #                                    color=colors[key],
                #                                    label=key))
                #
                #     # Sort and draw legend.
                #     labels, handles = zip(*sorted(zip(labels, handles),
                #                                   key=lambda x: x[0]))
                #     legend = plt.legend(handles, labels, loc=location,
                #                         title=r"Threshold ($\gamma$)")
                #     plt.setp(legend.get_title(), fontsize='xx-large')
                #
                #     if save:
                #         fig.savefig(path + "2." + ext)
                #     else:
                #         plt.show(fig)
                #
                #     # Allow disabling all plots under this block.
                #     pass
                #
                # # Allow disabling all plots under this block.
                # pass

            # =============================
            # Spiking Neural Networks Plots
            # =============================
            elif self.community_type == 'snn':

                # ---------------------------
                # Measures not involving Phi.
                # ---------------------------
                if run == 0:

                    # Coalition Entropy vs Weight and SCP
                    # -----------------------------------
                    for key in cursors:
                        fig = plt.figure()
                        ax = fig.gca(projection='3d')
                        ax.plot_trisurf(weight[key],
                                        scp[key],
                                        coalition_entropy[key],
                                        linewidth=0.2,
                                        cmap=cm.jet)
                        legend = plt.legend([], [],
                                            title=r"Threshold ($\gamma$) = " +
                                                  str(key))
                        plt.setp(legend.get_title(), fontsize='xx-large')
                        ax.set_xlabel(r"Weight ($W$)")
                        ax.set_ylabel(r"Connection Probability ($P$)")
                        ax.set_zlabel(r"Coalition Entropy ($H_C$)")
                        ax.set_xlim3d(0, 1)         # Weight
                        ax.set_ylim3d(0, 1)         # Connection Probability
                        ax.set_zlim3d(0, 2)         # Coalition Entropy

                        if save:
                            fig.savefig(path + "5." + ext)
                        else:
                            plt.show(fig)

                    # Lambda vs Weight and SCP
                    # ------------------------
                    for key in cursors:
                        fig = plt.figure()
                        ax = fig.gca(projection='3d')
                        ax.plot_trisurf(weight[key],
                                        scp[key],
                                        lamda[key],
                                        linewidth=0.2,
                                        cmap=cm.jet)
                        legend = plt.legend([], [],
                                            title=r"Threshold ($\gamma$) = " +
                                                  str(key))
                        plt.setp(legend.get_title(), fontsize='xx-large')
                        ax.set_ylabel(r"Synaptic Connection Probability ($P$)")
                        ax.set_xlabel(r"Weight ($W$)")
                        ax.set_zlabel(r"Metastability Index ($\lambda$)")
                        ax.set_xlim3d(0, 1)         # Weight
                        ax.set_ylim3d(0, 1)         # Connection Probability
                        ax.set_zlim3d(0, 0.08)      # Metastability Index

                        if save:
                            fig.savefig(path + "5." + ext)
                        else:
                            plt.show(fig)

                    # Global Synchrony vs Weight and SCP
                    # ----------------------------------
                    for key in cursors:
                        fig = plt.figure()
                        ax = fig.gca(projection='3d')
                        ax.plot_trisurf(weight[key],
                                        scp[key],
                                        global_sync[key],
                                        linewidth=0.2,
                                        cmap=cm.jet)
                        legend = plt.legend([], [],
                                            title=r"Threshold ($\gamma$) = " +
                                                  str(key))
                        plt.setp(legend.get_title(), fontsize='xx-large')
                        ax.set_xlabel(r"Weight ($W$)")
                        ax.set_ylabel(r"Synaptic Connection Probability ($P$)")
                        ax.set_zlabel(r"Global Synchrony ($\Psi$)")
                        ax.set_xlim3d(0, 1)         # Weight
                        ax.set_ylim3d(0, 1)         # Connection Probability
                        ax.set_zlim3d(0, 1)         # Global Synchrony

                        if save:
                            fig.savefig(path + "5." + ext)
                        else:
                            plt.show(fig)

                    # Allow disabling all plots under this block.
                    pass

                # Phi vs Weight and SCP
                # ---------------------
                for key in cursors:
                    fig = plt.figure()
                    ax = fig.gca(projection='3d')
                    location = 2
                    legend = plt.legend([], [], loc=location,
                                        title=r"$\gamma$ = " + str(key) + "\n" +
                                              r"$\tau$ = " + str(tau))
                    plt.setp(legend.get_title(), fontsize='xx-large')
                    ax.plot_trisurf(weight[key],
                                    scp[key],
                                    phi[key],
                                    linewidth=0.2,
                                    cmap=cm.jet)
                    ax.set_xlabel(r"Weight ($W$)")
                    ax.set_ylabel(r"Connection Probability ($P$)")
                    ax.set_zlabel(phi_label)
                    ax.set_xlim3d(0, 1)         # Weight
                    ax.set_ylim3d(0, 1)         # Connection Probability
                    if run == 0:
                        if tau == 1:
                            ax.set_zlim3d(-2.5, 0)
                        elif tau == 5:
                            ax.set_zlim3d(-1.5, 1)
                    else:
                        if tau == 1:
                            ax.set_zlim3d(0, 0.5)
                        elif tau == 5:
                            ax.set_zlim3d(0, 1.2)

                    if save:
                        fig.savefig(path + "5." + ext)
                    else:
                        plt.show(fig)

                # Allow disabling all plots under this block.
                pass

            run += 1

        # Phi Empirical vs Phi Empirical Tilde
        # ------------------------------------
        fig, ax = plt.subplots()
        handles = []
        labels = []
        for key in cursors:
            labels.append(key)
            handles.append(ax.scatter(phi_e[key],
                                      phi_e_tilde[key],
                                      color=colors[key],
                                      label=key))

        # Labels and axes.
        plt.xlabel(r"Empirical Integrated Information ($\Phi_{E}$)")
        plt.ylabel(r"Empirical Integrated Information Tilde "
                   r"($\widetilde{\Phi}_{E}$)")
        if self.community_type == 'oscillator' or \
           self.community_type == 'kuramoto':
            if tau == 1:
                plt.ylim(ymin=0, ymax=0.8)
                plt.xlim(xmin=-0.2, xmax=0.8)
        else:
            plt.ylim(ymin=0, ymax=1.2)
            plt.xlim(xmin=-2.2, xmax=0.6)
            plt.title(r"$\tau$ = " + str(tau))

        # Add whitespace.
        space = mlines.Line2D([], [], color='white', label='')
        handles.append(space)
        labels.append('')

        # Add Phi = Phi Tilde line.
        x = np.linspace(*ax.get_xlim())
        ax.plot(x, x, color='black', ls='dashed', lw=2)
        line = mlines.Line2D([], [], color='black', ls='dashed',
                             label=r'$\widetilde{\Phi}_{E} = \Phi_{E}$')
        handles.append(line)
        labels.append(r'$\widetilde{\Phi}_{E} = \Phi_{E}$')
        labels, handles = zip(*sorted(zip(labels, handles),
                                      key=lambda l: l[0]))
        legend = ax.legend(handles, labels, loc=2,
                           title=r"Threshold ($\gamma$)")
        plt.setp(legend.get_title(), fontsize='xx-large')

        if save:
            fig.savefig(path + "9." + ext)
        else:
            plt.show(fig)

        # Surrogate data plots.
        # =====================
        # if is_sorted or is_shuffled:
        #
        #     # Coalition Entropy Surrogate vs Coalition Entropy
        #     # ------------------------------------------------
        #     fig, ax = plt.subplots()
        #     handles = []
        #     labels = []
        #     for key in cursors:
        #         labels.append(key)
        #         plt.xlabel(r"Coalition Entropy ($H_C$)")
        #         plt.ylabel(r"Coalition Entropy Sorted ($H'_C$)")
        #         plt.ylim(ymin=-0.01, ymax=1)
        #         plt.xlim(xmin=0, xmax=1)
        #         handles.append(ax.scatter(hc_original[key],
        #                                   coalition_entropy[key],
        #                                   color=colors[key],
        #                                   label=key))
        #     # Add whitespace.
        #     space = mlines.Line2D([], [], color='white', label='')
        #     handles.append(space)
        #     labels.append('')
        #
        #     # Add H_C = H'_C line.
        #     x = np.linspace(*ax.get_xlim())
        #     ax.plot(x, x, color='black', ls='dashed', lw=2)
        #     line = mlines.Line2D([], [], color='black', ls='dashed',
        #                          label=r"$H_C = H'_C$")
        #     handles.append(line)
        #     labels.append(r"$H_C = H'_C$")
        #     labels, handles = zip(*sorted(zip(labels, handles),
        #                                   key=lambda x: x[0]))
        #     legend = ax.legend(handles, labels, loc=2,
        #                        title=r"Threshold ($\gamma$)")
        #     plt.setp(legend.get_title(), fontsize='xx-large')
        #     if save:
        #         fig.savefig(path + "7." + ext)
        #     else:
        #         plt.show(fig)
        #
        #     pass

        # Close all plots.
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
        plt.xlabel(r"Mutual Information for Original Data")
        plt.ylabel(r"Mutual Information for Shuffled Data")
        plt.xlim(xmin=0.002, xmax=0.012)
        plt.ylim(ymin=0.002, ymax=0.012)
        # plt.title("Mutual Information Analysis in Random Surrogate Data")
        plt.scatter(mi, mi_shuffled)
        if save:
            fig.savefig(path + "surrogate-random-mi-analysis." + ext)
        else:
            plt.show(fig)

        # Coalition Entropy Analysis
        fig = plt.figure()
        plt.xlabel(r"$H_C$ for Original Data")
        plt.ylabel(r"$H_C$ for Shuffled Data")
        # plt.title("Coalition Entropy Analysis in Random Surrogate Data")
        plt.scatter(hc, hc_shuffled)
        if save:
            fig.savefig(path + "surrogate-random-hc-analysis." + ext)
        else:
            plt.show(fig)

        # Integrated Information Empirical Analysis
        fig = plt.figure()
        plt.xlabel(r"Empirical Integrated Information ($\Phi_E$)"
                   r" for Original Data")
        plt.ylabel(r"Empirical Integrated Information ($\Phi_E$)"
                   r" for Shuffled Data")
        plt.xlim(xmin=0.002, xmax=0.012)
        plt.ylim(ymin=0.002, ymax=0.012)
        # plt.title("Integrated Information Analysis in Random Surrogate Data")
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
            "Empirical Integrated Information": phi_diff
        }

        fig = plt.figure()
        handles = []
        labels = []
        color = 0
        for key in measures:
            labels.append(key)
            plt.xlabel("Length of Pattern")
            plt.ylabel("Difference Between Original and Shuffled Data")
            # plt.title("Surrogate Analysis with Repeating Patterns")
            handles.append(plt.scatter(pattern_len,
                                       measures[key],
                                       color=self.colors[color],
                                       label=key))
            color += 1
        legend = plt.legend(handles, labels, loc=2, title="Measure")
        plt.setp(legend.get_title(), fontsize='xx-large')

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

    # Results for Kuramoto Oscillators
    # --------------------------------
    q = {
        'beta': {'$lte': (math.pi / 4)}
    }
    osc_thresholds = [0.9, 0.8, 0.7, 0.6, 0.5]
    dp = DataPlotter(community_type='kuramoto', database='infotheoretic')
    dp.plot(save=False,
            path="/Users/juancarlosfarah/Git/infotheoretic/docs/phi_e_tilde/",
            ext="svg",
            tau=20,
            query=q,
            thresholds=osc_thresholds)

    # Results for Spiking Neural Networks
    # -----------------------------------
    # dp = DataPlotter(community_type='snn', database='infotheoretic')
    # q_snn = {}
    # snn_thresholds = [0.95, 0.8]
    # dp.plot(save=False,
    #         path="/Users/juancarlosfarah/Git/infotheoretic/docs/phi_e_tilde/",
    #         ext="svg",
    #         tau=1,
    #         query=q_snn,
    #         thresholds=snn_thresholds)
    # dp.plot(save=False,
    #         path="/Users/juancarlosfarah/Git/infotheoretic/docs/phi_e_tilde/",
    #         ext="svg",
    #         tau=5,
    #         query=q_snn,
    #         thresholds=snn_thresholds)

    # Surrogate Data
    # --------------
    # dp = DataPlotter('oscillator', database='infotheoretic')
    # q = {
    #     'shuffled': {'$exists': True},
    #     'is_surrogate': False,
    #     'duration': 5000,
    #     'num_oscillators': 8,
    #     # 'beta': {'$lte': (math.pi / 4)}
    # }
    # osc_thresholds = [0.9, 0.8, 0.7, 0.6, 0.5]
    # dp.plot(save=False,
    #         path="/Users/juancarlosfarah/Git/infotheoretic/docs/phi_e_tilde/",
    #         ext="svg",
    #         tau=1,
    #         query=q,
    #         is_sorted=False,
    #         is_shuffled=True,
    #         thresholds=osc_thresholds)
    # dp.plot_surrogate_analysis()
    # dp.plot_normalised_surrogate()

    # Allow main code to be commented out.
    pass