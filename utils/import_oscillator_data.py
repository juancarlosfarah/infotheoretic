__author__ = 'juancarlosfarah'

import oct2py
import os
import pymongo
import numpy as np
import sys
import matrix_utils as mu
from bson.objectid import ObjectId
from threading import Thread


class OscillatorDataImporter:

    def __init__(self,
                 database=None,
                 is_surrogate=False,
                 is_shuffled=False,
                 is_sorted=False):
        self.db = database
        self.is_shuffled = is_shuffled
        self.is_sorted = is_sorted
        self.is_surrogate = is_surrogate or is_shuffled or is_sorted
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
        if not os.path.isdir(folder):
            raise NameError(folder)

        files = os.listdir(folder)

        # Files are by default Octave files.
        # Initialise Oct2Py object.
        oc = oct2py.Oct2Py()
        file_count = 0
        num_files = len(files)

        for f in files:
            if f.endswith(".mat"):
                path = folder + "/" + f
                output = oc.load(path)
                sync = output.data.sync
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
                for i in range(num_oscillators):
                    sync_vars.append(np.var(syncs[i]))

                # Compute variance for chi.
                chi_vars = []
                for i in range(duration):
                    chi_vars.append(np.var(syncs[:, i]))

                lamda = np.average(sync_vars)
                chi = np.average(chi_vars)
                avg_sync = np.average(avg_syncs)

                obj = {
                    "_id": _id,
                    "source": f,
                    "global_sync": avg_sync,
                    "beta": beta,
                    "lambda": lamda,
                    "chi": chi,
                    "num_oscillators": num_oscillators,
                    "duration": duration,
                    "threshold": threshold,
                    "is_surrogate": self.is_surrogate,
                    "is_shuffled": self.is_shuffled,
                    "is_sorted": self.is_sorted
                }

                # Shuffle if indicated.
                if self.is_shuffled:
                    np.random.shuffle(sync_discrete)

                # Sort if indicated.
                if self.is_sorted:
                    sync_reduced = mu.reduce(self.base, sync_discrete)
                    zipped = zip(sync_reduced, sync_discrete)
                    zipped.sort(key=lambda k: k[0])
                    sync_discrete = [v[1] for v in zipped]

                # Storing in MongoDB if database has been defined.
                db = self.db
                if db is not None:

                    # Create object container.
                    sync_objs = []
                    for data_point in sync_discrete:
                        # Store information in object.
                        sync_obj = {
                            "simulation_id": _id,
                            "data": data_point
                        }
                        sync_objs.append(sync_obj)

                    # Insert to database.
                    db.oscillator_simulation.insert_one(obj)
                    db.oscillator_data.insert(sync_objs, {'ordered': True})

                # Progress bar.
                file_count += 1
                progress = (file_count / float(num_files - 1)) * 100
                sys.stdout.write("Processing Oscillator Data: %d%% \r" % progress)
                sys.stdout.flush()

        return

if __name__ == '__main__':
    data_folder = "/Users/juancarlosfarah/Git/data/Data/part4"
    default_db = "infotheoretic"

    odi = OscillatorDataImporter()
    odi.connect(default_db)

    t1 = Thread(target=odi.load_folder, args=(data_folder, 0.9))
    t2 = Thread(target=odi.load_folder, args=(data_folder, 0.8))
    t3 = Thread(target=odi.load_folder, args=(data_folder, 0.7))
    t4 = Thread(target=odi.load_folder, args=(data_folder, 0.6))
    t5 = Thread(target=odi.load_folder, args=(data_folder, 0.5))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    # odi = OscillatorDataImporter(is_shuffled=True)
    # odi.connect(default_db)
    # odi.load_folder(data_folder, 0.9)
    # odi.load_folder(data_folder, 0.8)
    # odi.load_folder(data_folder, 0.7)
    # odi.load_folder(data_folder, 0.6)
    # odi.load_folder(data_folder, 0.5)