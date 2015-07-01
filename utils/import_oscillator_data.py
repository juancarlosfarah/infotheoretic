__author__ = 'juancarlosfarah'

import oct2py
import os
import pymongo
import numpy as np
import sys
from bson.objectid import ObjectId


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
                    sync_reduced = self.reduce(sync_discrete)
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

    def reduce(self, data):
        rows = len(data)
        columns = len(data[0])
        combined_values = []
        for r in range(rows):
            combined_row_value = 0
            multiplier = 1
            for c in range(columns - 1, -1, -1):
                # Add in the contribution from each row.
                combined_row_value += data[r][c] * multiplier
                multiplier *= self.base
            combined_values.append(combined_row_value)

        return combined_values


def test_reduce():
    odi = OscillatorDataImporter()
    d0 = np.array([[0, 0, 0, 0, 0, 1, 1, 0],
                   [1, 1, 1, 0, 0, 1, 1, 0],
                   [1, 1, 1, 0, 0, 1, 1, 0],
                   [0, 0, 1, 0, 1, 1, 1, 0],
                   [1, 1, 1, 0, 1, 0, 1, 1],
                   [0, 0, 1, 0, 1, 1, 1, 0]])

    d1 = [[0, 0, 0, 0, 0, 1, 1, 0],
          [1, 1, 1, 0, 0, 1, 1, 0],
          [1, 1, 1, 0, 0, 1, 1, 0],
          [0, 0, 1, 0, 1, 1, 1, 0],
          [1, 1, 1, 0, 1, 0, 1, 1],
          [0, 0, 1, 0, 1, 1, 1, 0]]

    # Should print out [26, 26, 31, 0, 7, 61, 63, 2]
    print odi.reduce(d0.T)

    d1 = np.array(d1).T
    d1 = d1.tolist()
    d1_reduced = odi.reduce(d1)
    zipped = zip(d1_reduced, d1)
    zipped.sort(key=lambda k: k[0])
    d1 = [v[1] for v in zipped]
    print np.array(d1)
    print d1_reduced
    print d1


def test_shuffle():
    odi = OscillatorDataImporter()

    d1 = [[0, 0, 0, 0, 0, 1, 1, 0],
          [1, 1, 1, 0, 0, 1, 1, 0],
          [1, 1, 1, 0, 0, 1, 1, 0],
          [0, 0, 1, 0, 1, 1, 1, 0],
          [1, 1, 1, 0, 1, 0, 1, 1],
          [0, 0, 1, 0, 1, 1, 1, 0]]

    # Should print out [26, 26, 31, 0, 7, 61, 63, 2]


    d1 = np.array(d1).T
    d1 = d1.tolist()
    d1_reduced = odi.reduce(d1)
    print d1_reduced

    zipped = zip(d1_reduced, d1)
    zipped.sort(key=lambda k: k[0])
    d1_sorted = [v[1] for v in zipped]
    print d1_sorted

    d1_reduced = odi.reduce(d1_sorted)
    print d1_reduced

    np.random.shuffle(d1_sorted)
    print d1_sorted
    d1_reduced = odi.reduce(d1_sorted)
    print d1_reduced

if __name__ == '__main__':
    data_folder = "/Users/juancarlosfarah/Git/data/Data"
    default_db = "infotheoretic"

    # odi = OscillatorDataImporter()
    # odi.connect(default_db)
    # odi.load_folder(data_folder, 0.9)
    # odi.load_folder(data_folder, 0.8)
    # odi.load_folder(data_folder, 0.7)
    # odi.load_folder(data_folder, 0.6)
    # odi.load_folder(data_folder, 0.5)

    # odi = OscillatorDataImporter(is_shuffled=True)
    # odi.connect(default_db)
    # odi.load_folder(data_folder, 0.9)
    # odi.load_folder(data_folder, 0.8)
    # odi.load_folder(data_folder, 0.7)
    # odi.load_folder(data_folder, 0.6)
    # odi.load_folder(data_folder, 0.5)