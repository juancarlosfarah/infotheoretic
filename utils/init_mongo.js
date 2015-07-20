/**
 * Created by juancarlosfarah on 07/06/15.
 */

// Create Indexes
// ==============
function createIndexes() {
    var db = db.getSiblingDB("infotheoretic");
    db.oscillator_data.ensureIndex({ "simulation_id": -1, "_id": 1 });
    db.generator_data.ensureIndex({ "simulation_id": -1, "_id": 1 });
}

// Remove Simulation Data
// =======================
function removeSimulationData(query) {

    var c = db.oscillator_simulation.find(query);

    while (c.hasNext()) {
        var doc = c.next();
        var sim_id = doc['_id'];
        db.oscillator_data.remove({"simulation_id": sim_id});
    }

    db.oscillator_simulation.remove(q);

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