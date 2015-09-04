__author__ = 'juancarlosfarah'

import pymongo
import numpy as np
import sys
from bson.objectid import ObjectId


class SurrogateDataGenerator:

    def __init__(self, database=None):
        self.base = 2

        # Connect to MongoDB database.
        if database is not None:
            host = "localhost"
            port = 27017
            mc = pymongo.MongoClient(host=host, port=port)
            self.db = mc.get_database(database)

    def generate(self, pattern, duration=5000):

        pattern_length = len(pattern)

        # Don't generate empty time series.
        if pattern_length == 0:
            return

        _id = ObjectId()
        num_vars = len(pattern[0])

        sim = {
            "_id": _id,
            "num_vars": num_vars,
            "duration": duration,
            "pattern": pattern
        }

        data = []
        main_it = duration / pattern_length
        rem_it = duration % pattern_length

        for i in range(main_it):
            data.extend(pattern)

        for j in range(rem_it):
            data.append(pattern[j])

        self.store(sim, data)

    # noinspection PyUnresolvedReferences
    def generate_random(self, num_vars, duration=5000):

        _id = ObjectId()

        sim = {
            "_id": _id,
            "num_vars": num_vars,
            "duration": duration,
            "pattern": "random"
        }

        data = np.random.rand(duration, num_vars)
        data[data < 0.5] = 0
        data[data >= 0.5] = 1
        data = data.tolist()

        self.store(sim, data)

    def store(self, sim, data):

        if '_id' not in sim:
            return

        _id = sim['_id']
        duration = sim['duration']

        # Storing in MongoDB if database has been defined.
        db = self.db
        if db is not None:

            # Create object container.
            data_objs = []

            dp_count = 0
            for data_point in data:

                # Store information in object.
                sync_obj = {
                    "simulation_id": _id,
                    "data": data_point
                }
                data_objs.append(sync_obj)

                # # Progress bar.
                dp_count += 1
                prog = (dp_count / float(duration - 1)) * 100
                sys.stdout.write("Generating Surrogate Data: %d%% \r" % prog)
                sys.stdout.flush()

            # Insert to database.
            db.generator_simulation.insert_one(sim)
            db.generator_data.insert(data_objs, {'ordered': True})


if __name__ == '__main__':
    sdg = SurrogateDataGenerator("infotheoretic")

    # One state.
    # pattern = [[0, 0, 0]]
    # sdg.generate(pattern=pattern)

    # # Oscillate between two states.
    # pattern = [[0, 0, 0], [1, 1, 1]]
    # sdg.generate(pattern=pattern)

    # # Oscillate between three states.
    # pattern = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    # sdg.generate(pattern=pattern)

    # Oscillate between four states.
    # pattern = [[0, 0, 0], [0, 1, 0], [0, 1, 1], [1, 1, 1]]
    # sdg.generate(pattern=pattern)

    #  Oscillate between five states.
    # pattern = [[0, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1], [1, 1, 1]]
    # sdg.generate(pattern=pattern)
    #
    # #  Oscillate between six states.
    # pattern = [[0, 0, 0],
    #            [0, 0, 1],
    #            [0, 1, 0],
    #            [0, 1, 1],
    #            [1, 0, 0],
    #            [1, 0, 1]]
    # sdg.generate(pattern=pattern)
    #
    # #  Oscillate between seven states.
    # pattern = [[0, 0, 0],
    #            [0, 0, 1],
    #            [0, 1, 0],
    #            [0, 1, 1],
    #            [1, 0, 0],
    #            [1, 0, 1],
    #            [1, 1, 0]]
    # sdg.generate(pattern=pattern)

    # # Visit all states.
    # pattern = [[0, 0, 0],
    #            [0, 0, 1],
    #            [0, 1, 0],
    #            [0, 1, 1],
    #            [1, 0, 0],
    #            [1, 0, 1],
    #            [1, 1, 0],
    #            [1, 1, 1]]
    # sdg.generate(pattern=pattern)

    # Generate random pattern.
    # sdg.generate_random(3, 5000)