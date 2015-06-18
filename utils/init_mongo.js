/**
 * Created by juancarlosfarah on 07/06/15.
 */

// Create Indexes
// ==============
var db = db.getSiblingDB("infotheoretic");
db.oscillator_data.ensureIndex({ "simulation_id": -1, "_id": 1 });

// Remove Surrogate Data
// =====================
var c = db.oscillator_simulation.find({"is_surrogate": true});

while (c.hasNext()) {
    var doc = c.next();
    var sim_id = doc['_id'];
    db.oscillator_data.remove({"simulation_id": sim_id});
}

db.oscillator_simulation.remove({"is_surrogate": true});