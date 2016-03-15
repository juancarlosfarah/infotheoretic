__author__ = 'juancarlosfarah'

import oct2py
import os
import pymongo
import numpy as np
import scipy.stats as st
import sys
from bson.objectid import ObjectId


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
    def load_folder(self, folder):
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
                lambda_skew = np.average(sync_vars_skew)
                chi = np.average(chi_vars)
                avg_sync = np.average(avg_syncs)

                obj = {
                    "_id": _id,
                    "source": f,
                    "global_sync": avg_sync,
                    "beta": beta,
                    "lambda": lamda,
                    "lambda_skew": lambda_skew,
                    "chi": chi,
                    "num_oscillators": num_oscillators,
                    "duration": duration
                }

                # Storing in MongoDB if database has been defined.
                db = self.db
                if db is not None:

                    # Create object container.
                    sync_objs = []
                    for i in range(duration):
                        data = syncs[:, i].tolist()

                        # Store information in object.
                        sync_obj = {
                            "simulation_id": _id,
                            "data": data
                        }
                        sync_objs.append(sync_obj)

                    # Insert to database.
                    db.k_simulation.insert_one(obj)
                    db.k_data.insert(sync_objs, {'ordered': True})

                # Progress bar.
                file_count += 1
                progress = (file_count / float(num_files - 1)) * 100
                sys.stdout.write("Processing Kuramoto Data: %d%% \r" % progress)
                sys.stdout.flush()

        return

if __name__ == '__main__':

    default_db = "infotheoretic"

    kdi = KuramotoDataImporter()
    kdi.connect(default_db)

    # Import data.
    # ------------
    for i in range(1, 7):
        data_folder = "/Users/juancarlosfarah/Git/data/Data/part" + str(i)
        kdi.load_folder(data_folder)