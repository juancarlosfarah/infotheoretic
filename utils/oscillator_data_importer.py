__author__ = 'juancarlosfarah'

import oct2py
import os
import pymongo
import numpy as np
import scipy.stats as st
import sys
from bson.objectid import ObjectId
from threading import Thread


class KuramotoDataImporter:

    def __init__(self, database=None):
        self.db = database
        self.base = 2

    def connect(self, database):
        """
        Connect to MongoDB database.
        :param database: Database name.
        :return: Handle to database.
        """
        host = "localhost"
        port = 27017
        mc = pymongo.MongoClient(host=host, port=port)
        self.db = mc.get_database(database)
        return self.db

    # noinspection PyUnresolvedReferences
    def load_folder(self, folder, threshold):
        print "Loading folder..."

        if not os.path.isdir(folder):
            raise NameError(folder)

        files = os.listdir(folder)

        # Files are by default Octave files.
        # Initialise Oct2Py object.
        oc = oct2py.Oct2Py()
        file_count = 0
        num_files = len(files)

        # Length of transient period (200 time steps equals 1s).
        transient = 200

        print "Preparing to load " + str(num_files) + " files..."
        for f in files:
            if f.endswith(".mat"):
                print "Processing file " + f
                path = folder + "/" + f
                output = oc.load(path)
                sync = output.data.sync[transient:]
                duration = len(sync)
                num_oscillators = sync[0].shape[0]
                avg_syncs = []
                beta = output.data.b
                sync_discrete = []
                syncs = np.zeros((num_oscillators, duration))

                # Create ObjectId
                _id = ObjectId()

                t_step = 0
                for sync_t in sync:

                    # Record average synchrony to calculate global synchrony.
                    avg_sync_t = np.average(sync_t)
                    avg_syncs.append(avg_sync_t)

                    # Get diagonal and store for later calculations.
                    diagonal = sync_t.diagonal().copy()
                    syncs[:, t_step] = diagonal.T

                    # Transform diagonal.
                    diagonal[diagonal < threshold] = 0
                    diagonal[diagonal >= threshold] = 1
                    data = diagonal.tolist()

                    sync_discrete.append(data)
                    t_step += 1

                # Compute variance for lambda.
                sync_vars = []
                skews = []
                sync_vars_skew = []
                for i in range(num_oscillators):
                    sync_vars.append(np.var(syncs[i]))
                    skews.append(st.skew(syncs[i]))
                    skw_factor = 1.0 - abs(skews[i]) / 2.0
                    if skw_factor < 0:
                        skw_factor = 0
                    sync_vars_skew.append(sync_vars[i] * skw_factor)

                # Compute variance for chi.
                chi_vars = []
                for i in range(duration):
                    chi_vars.append(np.var(syncs[:, i]))

                lamda = np.average(sync_vars)
                lamda_skew = np.average(sync_vars_skew)
                chi = np.average(chi_vars)
                avg_sync = np.average(avg_syncs)

                obj = {
                    "_id": _id,
                    "source": f,
                    "global_sync": avg_sync,
                    "beta": beta,
                    "lambda": lamda,
                    "lambda_skew": lamda_skew,
                    "chi": chi,
                    "num_oscillators": num_oscillators,
                    "duration": duration,
                    "threshold": threshold
                }

                # Storing in MongoDB if database has been defined.
                db = self.db
                if db is not None:

                    # Create object container.
                    sync_objs = []
                    for i in range(duration):
                        data_continuous = syncs[:, i].tolist()
                        data_discrete = sync_discrete[i]

                        # Store information in object.
                        sync_obj = {
                            "simulation_id": _id,
                            "discrete": data_discrete,
                            "continuous": data_continuous
                        }
                        sync_objs.append(sync_obj)

                    # Insert to database.
                    db.kuramoto_simulation.insert_one(obj)
                    db.kuramoto_data.insert(sync_objs, {'ordered': True})

                # Progress bar.
                file_count += 1
                progress = (file_count / float(num_files - 1)) * 100
                sys.stdout.write("Processing Kuramoto Data: %d%% \r" % progress)
                sys.stdout.flush()

        return

if __name__ == '__main__':
    data_folder = "/Users/juancarlosfarah/Git/data/Data/part#"
    default_db = "infotheoretic"

    kdi = KuramotoDataImporter()
    kdi.connect(default_db)

    # Use multiple threads.
    # ---------------------
    # t1 = Thread(target=kdi.load_folder, args=(data_folder, 0.9))
    # t2 = Thread(target=kdi.load_folder, args=(data_folder, 0.8))
    # t3 = Thread(target=kdi.load_folder, args=(data_folder, 0.7))
    # t4 = Thread(target=kdi.load_folder, args=(data_folder, 0.6))
    # t5 = Thread(target=kdi.load_folder, args=(data_folder, 0.5))
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    #
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()

    # Use single threads.
    # ---------------------
    kdi.load_folder(data_folder, 0.9)
    kdi.load_folder(data_folder, 0.8)
    kdi.load_folder(data_folder, 0.7)
    kdi.load_folder(data_folder, 0.6)
    kdi.load_folder(data_folder, 0.5)