/**
 * Created by juancarlosfarah on 07/06/15.
 */

// Create Indexes
// ==============
function createIndexes() {
    var db = db.getSiblingDB("infotheoretic");
    db.oscillator_data.ensureIndex({ "simulation_id": -1, "_id": 1 });
    db.generator_data.ensureIndex({ "simulation_id": -1, "_id": 1 });
    db.snn_data.ensureIndex({ "simulation_id": -1, "_id": 1 });
    db.snn_simulation.ensureIndex({ "source": 1 });
}

// Remove Simulation Data
// =======================
function removeSimulationData(type, query) {
    var simCollectionName = type + "_simulation";
    var dataCollectionName = type + "_data";
    var simCollection = db[simCollectionName];
    var dataCollection = db[dataCollectionName];
    var c = simCollection.find(query);

    while (c.hasNext()) {
        var doc = c.next();
        var sim_id = doc['_id'];
        dataCollection.remove({"simulation_id": sim_id});
    }

    simCollection.remove(query);

}

// Copy Data
// =========
function duplicate() {
    var c = db.oscillator_simulation.find({"is_surrogate": true}, {"_id": 0});

    while (c.hasNext()) {
        var doc = c.next();
        doc["is_sorted"] = true;
        db.oscillator_data.insert(doc);
    }
}

// Count number of data points per simulation.
// ===========================================
db.generator_data.aggregate([ { "$group": { "_id": "$simulation_id",
                                            "sum": { "$sum": 1 }}}]);

// Useful commands
// ===============
db.snn_simulation.find({ "source": /part1/}).count();
db.snn_simulation.find({ "source": /part1/}).sort({"_id": -1}).limit(1).pretty();
removeSimulationData("snn", { "source": /^gamma\-0\.95\/part1/ });

// Transform Data
// ==============
function transform(collectionName) {
    var collection = db[collectionName];
    var c = collection.find({});
    while (c.hasNext()) {
        var doc = c.next();
        var _id = doc['_id'];
        var subdoc = {
            "phi_e": doc['phi_e'],
            "phi_e_tilde": doc['phi_e_tilde'],
            "mib": doc['mib'],
            "mib_tilde": doc['mib_tilde'],
            "mi": doc['mi'],
            "tau": 1
        };
        collection.update({ "_id": _id }, { "$set": { "tau_1": subdoc } });
    }
}