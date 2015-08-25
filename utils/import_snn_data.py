__author__ = 'juancarlosfarah'

import oct2py
import os
import pymongo
import numpy as np
import sys
from bson.objectid import ObjectId


def find_largest_coalition(previous, current):
    """
    Returns the largest coalition given a current set of
    coalitions and the previous largest coalition.
    :param previous: List containing previous largest coalition.
    :param current: Numpy array containing the set of current coalitions.
    :return: List containing current largest coalition.
    """

    # Record largest coalition.
    largest_coalition = []

    # Iterate through all coalitions to find the largest.
    for coalition in current:
        c = coalition[0]

        if len(c) > len(largest_coalition):
            largest_coalition = c

        # If two coalitions have the same length, choose
        # the one that resembles the previous one the most.
        elif len(c) == len(largest_coalition):
            score_new = np.intersect1d(c, previous, True).size
            score_old = np.intersect1d(largest_coalition, previous, True).size
            if score_new > score_old:
                largest_coalition = c

            # If both resemble the previous one equally, choose a random one.
            elif score_new == score_old:
                flip = np.random.randint(2)
                if flip == 0:
                    largest_coalition = c

    return largest_coalition


class SpikingNeuralNetworkDataImporter:

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
        if not os.path.isdir(folder):
            raise NameError(folder)

        files = os.listdir(folder)

        # Files are by default Octave files.
        # Initialise Oct2Py object.
        oc = oct2py.Oct2Py()
        file_count = 0
        num_files = len(files)

        for f in files:
            if f.endswith(".mat") and "FiringsCoal" in f:
                path = folder + "/" + f
                output = oc.load(path)
                scp = output.sp
                weight = output.w
                coalition_jumpers = float(output.finalFitness[0])
                coalition_entropy = float(output.finalFitness[1])
                global_sync = float(output.finalFitness[3])
                lamda_skew_fix = float(output.finalFitness[4])
                lamda = float(output.finalFitness[5])
                num_communities = 10
                duration = len(output.finalFitness[6])
                source = path.split("snn/")[1]
                coalitions = output.finalFitness[6]
                db = self.db
                sync_objs = []

                # Create ObjectId
                _id = ObjectId()

                # Start with a previous coaltion containing all of
                previous_coalition = [x for x in range(1, 11)]

                for coalition in coalitions:

                    # Sanitise data.
                    c = coalition[0]

                    # Get largest coalition.
                    lc = find_largest_coalition(previous_coalition, c)

                    # Prepare discrete synchronisation array.
                    sync = [0] * 10
                    for i in lc:
                        sync[int(i - 1)] = 1

                    # Populate array for store if database has been defined.
                    if db is not None:
                        sync_obj = {
                            "simulation_id": _id,
                            "data": sync
                        }
                        sync_objs.append(sync_obj)

                    # Update previous largest coalition.
                    previous_coalition = lc

                # Storing in MongoDB if database has been defined.
                if db is not None:

                    # Create simulation object.
                    obj = {
                        "_id": _id,
                        "source": source,
                        "global_sync": global_sync,
                        "synaptic_connection_probability": scp,
                        "weight": weight,
                        "coalition_entropy": coalition_entropy,
                        "coalition_jumpers": coalition_jumpers,
                        "lambda": lamda,
                        "lambda_skew_fix": lamda_skew_fix,
                        "num_communities": num_communities,
                        "duration": duration,
                        "threshold": threshold
                    }

                    db.snn_simulation.insert_one(obj)
                    db.snn_data.insert(sync_objs, {'ordered': True})

                # Progress bar.
                file_count += 1
                progress = (file_count / float(num_files - 1)) * 100
                sys.stdout.write("Processing Spiking Neural Network Data: %d%% "
                                 "\r" % progress)
                sys.stdout.flush()

        return


if __name__ == '__main__':
    data_folder = "/Users/juancarlosfarah/Git/data/snn/gamma-0.8/part1"
    default_db = "infotheoretic"

    snndi = SpikingNeuralNetworkDataImporter()
    snndi.connect(default_db)
    snndi.load_folder(data_folder, 0.8)