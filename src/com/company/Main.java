package com.company;

import com.google.common.primitives.Ints;
import com.mongodb.MongoClient;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import infodynamics.measures.discrete.MutualInformationCalculatorDiscrete;
import infodynamics.measures.discrete.EffectiveInformationCalculatorDiscrete;
import infodynamics.measures.discrete
                   .IntegratedInformationEmpiricalCalculatorDiscrete;
import infodynamics.measures.discrete
                   .IntegratedInformationEmpiricalTildeCalculatorDiscrete;
import infodynamics.utils.MatrixUtils;
import infodynamics.utils.RandomGenerator;
import infodynamics.utils.Input;
import org.bson.Document;
import org.bson.types.ObjectId;

import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Sorts.ascending;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {

    public static void testMutualInformation() {

        System.out.println("Testing mutual information...");

        int[] var0 = { 0, 1, 1, 0 };
        int[] var1 = { 0, 1, 1, 0 };
        int[] var2 = { 0, 0, 1, 1 };

        try {
            MutualInformationCalculatorDiscrete micd = new
                    MutualInformationCalculatorDiscrete(2);
            micd.addObservations(var0, var1);

            System.out.println(micd.computeAverageLocalOfObservations());
            micd.addObservations(var0, var2);

            micd.initialise();
            System.out.println(micd.computeAverageLocalOfObservations());
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("\n");

    }

    public static void testMutualInformationTimeSeries() {

        System.out.println("Testing mutual information on time series...");

        int[] var0 = { 0, 0, 0, 0, 0, 1, 1, 0};
        int[] var1 = { 1, 1, 1, 0, 0, 1, 1, 0};
        int[] var2 = { 1, 1, 1, 0, 0, 1, 0, 0};
        int[] var3 = { 0, 0, 1, 0, 1, 1, 1, 0};
        int[] var4 = { 1, 1, 1, 0, 1, 0, 1, 1};
        int[] var5 = { 0, 0, 1, 0, 1, 1, 1, 0};

        int[][] states = { var0, var1, var2, var3, var4, var5 };

        try {
            MutualInformationCalculatorDiscrete micd = new
                    MutualInformationCalculatorDiscrete(2, 0);

            for (int i = 1; i < states[0].length; i++) {
                micd.initialise();
                micd.addObservations(states, i - 1, i);
                System.out.println(micd.computeAverageLocalOfObservations());
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("\n");

    }

    public static void testMutualInformationTimeSeriesPairs() {

        System.out.println("Testing MI on time series pairs...");

        int[] var0 = { 0, 0, 0, 0, 0, 1, 1, 0, 0, 1 };
        int[] var1 = { 1, 1, 1, 0, 0, 1, 1, 0, 0, 1 };
        int[] var2 = { 1, 1, 1, 0, 0, 1, 1, 0, 0, 1 };
        int[] var3 = { 0, 0, 1, 0, 1, 1, 1, 0, 0, 1 };
        int[] var4 = { 1, 1, 1, 0, 1, 0, 1, 1, 0, 1 };
        int[] var5 = { 0, 0, 1, 0, 1, 1, 1, 0, 0, 1 };

        int iterations = 5;

        int[][] states = new int[6][10 * iterations];

        for (int i = 0; i < iterations; i++) {
            int index = i * 10;
            for (int j = 0; j < 10; j++) {
                states[0][index + j] = var0[j];
                states[1][index + j] = var1[j];
                states[2][index + j] = var2[j];
                states[3][index + j] = var3[j];
                states[4][index + j] = var4[j];
                states[5][index + j] = var5[j];
            }
        }

        Input input = new Input(states, 2);

        // Pair using tau = 1.
        int tau = 1;
        int[][] paired = input.pair(tau);
        System.out.println(input);

        try {
            MutualInformationCalculatorDiscrete micd = new
                    MutualInformationCalculatorDiscrete(input.getReducedBase(),
                                                        0);

            micd.initialise();
            micd.addObservations(paired[0], paired[1]);
            System.out.println(micd.computeAverageLocalOfObservations());

        } catch (Exception e) {
            e.printStackTrace();
        }

        // All states in three variables being visited.
        int[] var6 = { 0, 0, 0, 1, 1, 1, 0, 1};
        int[] var7 = { 0, 0, 1, 1, 0, 0, 1, 1};
        int[] var8 = { 0, 1, 1, 0, 0, 1, 0, 1};

        int it = 200;

        int[][] states1 = new int[3][8 * it];

        for (int i = 0; i < it; i++) {
            int index = i * 8;
            for (int j = 0; j < 8; j++) {
                states1[0][index + j] = var6[j];
                states1[1][index + j] = var7[j];
                states1[2][index + j] = var8[j];
            }
        }

        Input input1 = new Input(states1, 2);

        int[][] paired1 = input1.pair(tau);
        System.out.println(input1);

        try {
            MutualInformationCalculatorDiscrete micd = new
                    MutualInformationCalculatorDiscrete(input1.getReducedBase(),
                    0);

            micd.initialise();
            micd.addObservations(paired1[0], paired1[1]);
            System.out.println(micd.computeAverageLocalOfObservations());

        } catch (Exception e) {
            e.printStackTrace();
        }

        int[] var09 = { 0, 0, 0, 0, 0, 0, 0, 0 };
        int[] var10 = { 0, 0, 0, 0, 0, 0, 0, 0 };
        int[] var11 = { 0, 1, 0, 1, 0, 1, 0, 1 };

        int iter = 200;

        int[][] states2 = new int[3][8 * iter];

        for (int i = 0; i < iter; i++) {
            int index = i * 8;
            for (int j = 0; j < 8; j++) {
                states2[0][index + j] = var09[j];
                states2[1][index + j] = var10[j];
                states2[2][index + j] = var11[j];
            }
        }

        // Repeating states in three variable system.
        Input input2 = new Input(states2, 2);

        int[][] paired2 = input2.pair(tau);
        System.out.println(input2);

        try {
            MutualInformationCalculatorDiscrete micd = new
                    MutualInformationCalculatorDiscrete(input1.getReducedBase(),
                    0);

            micd.initialise();
            micd.addObservations(paired2[0], paired2[1]);
            System.out.println(micd.computeAverageLocalOfObservations());

        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("\n");

    }

    public static void testIntegratedInformation() {

        // Use tau = 1;
        int tau = 1;

        // Example adapted from Wikipedia article on IIT.
        // https://en.wikipedia.org/wiki/Integrated_information_theory
        System.out.println("First Effective Information Test:");

        // Generate model.
        RandomGenerator rg = new RandomGenerator();
        int duration = 1000000;
        int[] var0a = rg.generateRandomInts(duration, 2);
        var0a[0] = 0;
        int[] var1a = new int[duration];
        var1a[0] = 0;
        System.arraycopy(var0a, 0, var1a, 1, duration - 1);
        int[][] states0 = {var0a, var1a};

        // Compute EI for original generative model.
        EffectiveInformationCalculatorDiscrete eicd;
        eicd = new EffectiveInformationCalculatorDiscrete(2, tau);
        eicd.addObservations(states0);
        System.out.println("Computing EI for original generative model:");
        double s = eicd.computeMutualInformationForSystem();
        System.out.println("System:\t\t\t" + s);
        int[] p0 = {0};
        double o0 = eicd.computeForBipartition(p0);
        System.out.println("Partition 1:\t" + o0);
        int[] p1 = {1};
        double o1 = eicd.computeForBipartition(p1);
        System.out.println("Partition 2:\t" + o1);

        // Compute II for original generative model.
        System.out.println("Computing II for original generative model:");
        IntegratedInformationEmpiricalCalculatorDiscrete iicd;
        iicd = new IntegratedInformationEmpiricalCalculatorDiscrete(2, tau);
        iicd.addObservations(states0);
        iicd.computePossiblePartitions();
        System.out.println(iicd.compute());
        System.out.println(Arrays.deepToString(iicd.minimumInformationPartition));
        System.out.println();

        // Shuffle data.
        int[][] states0s = MatrixUtils.shuffle(states0);
        eicd = new EffectiveInformationCalculatorDiscrete(2, tau);
        eicd.addObservations(states0s);

        // Compute EI for shuffled generative model.
        System.out.println("Computing EI for shuffled generative model:");
        double ss = eicd.computeMutualInformationForSystem();
        System.out.println("System:\t\t\t" + ss);
        int[] p0s = {0};
        double o0s = eicd.computeForBipartition(p0s);
        System.out.println("Partition 1:\t" + o0s);
        int[] p1s = {1};
        double o1s = eicd.computeForBipartition(p1s);
        System.out.println("Partition 2:\t" + o1s);

        // Compute II for shuffled generative model.
        System.out.println("Computing II for shuffled generative model:");
        iicd = new IntegratedInformationEmpiricalCalculatorDiscrete(2, tau);
        iicd.addObservations(states0s);
        iicd.computePossiblePartitions();
        System.out.println(iicd.compute());
        System.out.println(Arrays.deepToString(iicd.minimumInformationPartition));


        System.out.println("\n");
        System.out.println("Second Effective Information Test:");

        int[] var4  = {1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1};
        int[] var5  = {0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1};
        int[] var6  = {0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0};
        int[] var7  = {1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1};
        int[] var8  = {0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1};
        int[] var9  = {1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1};
        int[] var10 = {1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0};
        int[] var11 = {1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1};

        int[][] states1 = {var4, var5, var6, var7, var8, var9, var10, var11};

        eicd.addObservations(states1);

        int[] p2 = {0, 1, 2};
        double o2 = eicd.computeForBipartition(p2);
        System.out.println(o2);

        System.out.println("\n");
        System.out.println("First Integrated Information Test:");

        iicd = new IntegratedInformationEmpiricalCalculatorDiscrete(2, tau);
        iicd.addObservations(states1);
        iicd.computePossiblePartitions();

        System.out.println(iicd.compute());
        System.out.println(Arrays.deepToString(iicd.minimumInformationPartition));

        System.out.println("\n");
        System.out.println("Second Integrated Information Test:");

        int[][] states2 = rg.generateRandomInts(8, 10000, 2);

        iicd = new IntegratedInformationEmpiricalCalculatorDiscrete(2, tau);
        iicd.addObservations(states2);
        iicd.computePossiblePartitions();
        System.out.println(iicd.compute());
        System.out.println(Arrays.deepToString(iicd.minimumInformationPartition));

    }

    public static void testCoalitionEntropy() {

        System.out.println("\n");
        System.out.println("Coalition Entropy Test:");

        CoalitionEntropyCalculatorDiscrete cecd;
        cecd = new CoalitionEntropyCalculatorDiscrete(2);

        int[] var1 = {1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1};
        int[] var2 = {1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0};
        int[] var3 = {1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1};
        int[] var4 = {1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1};

        int[][] states = {var1, var2, var3, var4};

        cecd.addObservations(states);

        System.out.println(cecd);
        System.out.println(cecd.compute());
    }

    public static void computeIntegratedInformation(String type,
                                                    int tau,
                                                    boolean override,
                                                    boolean shuffle,
                                                    boolean save) {

        IntegratedInformationEmpiricalCalculatorDiscrete iicd;
        IntegratedInformationEmpiricalTildeCalculatorDiscrete iicdt;

        // Test with data from Kuramoto Oscillator simulations.
        String host = "localhost";
        int port = 27017;
        String database = "infotheoretic";
        MongoClient mongoClient = new MongoClient(host, port);
        MongoDatabase db = mongoClient.getDatabase(database);
        MongoCollection<Document> simulation;
        MongoCollection<Document> data;
        simulation = db.getCollection(type + "_simulation");
        data = db.getCollection(type + "_data");
        String tauKey = "tau_" + tau;

        Document query = new Document();
        if (!override) {
            Document ne = new Document("$exists", false);
            query.put(tauKey, ne);
        }

        // Counter to keep track of number of updated documents.
        int count = 0;

        for (Document doc : simulation.find(query)) {

            // Get ObjectId for simulation.
            ObjectId _id = doc.getObjectId("_id");

            // Get data for this simulation.
            MongoCursor<Document> cursor = data.find(eq("simulation_id", _id))
                                               .sort(ascending("_id"))
                                               .iterator();
            int num_communities;
            if (type.equals("oscillator") || type.equals("kuramoto")) {
                num_communities = doc.getInteger("num_oscillators");
            } else {
                num_communities = doc.getInteger("num_communities");
            }

            int duration = doc.getInteger("duration");
            int[][] obs = new int[num_communities][duration * 10];

            // Transform data for use with Phi_E Calculator.
            int column = 0;
            while (cursor.hasNext()) {
                Document d = cursor.next();
                ArrayList<Integer> array = (ArrayList) (d.get("data"));
                int[] vector = Ints.toArray(array);
                MatrixUtils.insertVectorIntoMatrix(vector, obs, column);
                for (int i = 1; i < 10; i++) {
                    MatrixUtils.insertVectorIntoMatrix(vector,
                                                       obs,
                                                       column + i * duration);
                }
                column++;
            }

            // Compute Phi_E and Minimum Information Bipartition.
            iicd = new IntegratedInformationEmpiricalCalculatorDiscrete(2, tau);
            iicd.addObservations(obs);
            iicd.computePossiblePartitions();
            double ii = iicd.compute();
            double mi = iicd.getMutualInformation();
            ArrayList<List<Integer>> mib = new ArrayList<List<Integer>>();
            mib.add(Ints.asList(iicd.minimumInformationPartition[0]));
            mib.add(Ints.asList(iicd.minimumInformationPartition[1]));

            // Compute Phi_E Tilde and Minimum Information Bipartition.
            iicdt = new IntegratedInformationEmpiricalTildeCalculatorDiscrete(2,
                    tau);
            iicdt.addObservations(obs);
            iicdt.computePossiblePartitions();
            double ii_tilde = iicdt.compute();
            ArrayList<List<Integer>> mib_tilde = new ArrayList<List<Integer>>();
            mib_tilde.add(Ints.asList(iicd.minimumInformationPartition[0]));
            mib_tilde.add(Ints.asList(iicd.minimumInformationPartition[1]));

            // Store results in MongoDB.
            if (save) {

                // Initialise documents.
                Document setDoc = new Document();
                Document update = new Document();
                Document tauDoc = new Document();

                // Populate fields.
                update.put("phi_e", ii);
                update.put("mib", mib);
                update.put("mi", mi);
                update.put("phi_e_tilde", ii_tilde);
                update.put("mib_tilde", mib_tilde);
                update.put("tau", tau);

                // Put update in embedded document.
                tauDoc.put(tauKey, update);
                setDoc.put("$set", tauDoc);
                simulation.updateOne(eq("_id", _id), setDoc);
            }

            // Show counter.
            count++;
            System.out.println("Finished processing simulation #" + count +
                               " with ID: " + _id);
            cursor.close();
        }

        // Disconnect from DB.
        mongoClient.close();

    }

    public static void computeCoalitionEntropy(boolean override) {

        int base = 2;
        CoalitionEntropyCalculatorDiscrete cecd;

        // Test with data from Kuramoto Oscillator simulations.
        String host = "localhost";
        int port = 27017;
        String database = "infotheoretic";
        MongoClient mongoClient = new MongoClient(host, port);
        MongoDatabase db = mongoClient.getDatabase(database);
        MongoCollection<Document> simulation;
        MongoCollection<Document> data;
        simulation = db.getCollection("kuramoto_simulation");
        data = db.getCollection("kuramoto_data");

        Document query = new Document();
        Document ne = new Document("$exists", override);
        query.put("coalition_entropy", ne);

        // Counter to keep track of number of updated documents.
        int count = 0;

        for (Document doc : simulation.find(query)) {

            // Get ObjectId for simulation.
            ObjectId _id = doc.getObjectId("_id");

            // Get data for this simulation.
            MongoCursor<Document> cursor = data.find(eq("simulation_id", _id))
                                               .sort(ascending("_id"))
                                               .iterator();
            int num_oscillators = doc.getInteger("num_oscillators");
            int duration = doc.getInteger("duration");
            int[][] obs = new int[num_oscillators][duration];

            // Transform data for use with H_c Calculator.
            int column = 0;
            while (cursor.hasNext()) {
                Document d = cursor.next();
                ArrayList<Integer> array = (ArrayList) (d.get("data"));
                int[] vector = Ints.toArray(array);
                MatrixUtils.insertVectorIntoMatrix(vector, obs, column);
                column++;
            }

            // Compute coalition entropy.
            cecd = new CoalitionEntropyCalculatorDiscrete(base);
            cecd.addObservations(obs);
            double ce = cecd.compute();

            // Store results in MongoDB.
            Document setDoc = new Document();
            Document update = new Document();
            update.put("coalition_entropy", ce);
            setDoc.put("$set", update);

            simulation.updateOne(eq("_id", _id), setDoc);

            // Show counter.
            count++;
            System.out.println("Finished processing simulation " + count + ".");
            cursor.close();
        }

        // Disconnect from DB.
        mongoClient.close();
    }

    public static MongoDatabase connect() {
        String host = "localhost";
        int port = 27017;
        String database = "infotheoretic";
        MongoClient mongoClient = new MongoClient(host , port);
        MongoDatabase db = mongoClient.getDatabase(database);
        return db;
    }

    public static void getSimulationData(MongoCollection<Document> data,
                                         ObjectId _id,
                                         int[][] obs) {

        MongoCursor<Document> cursor = data.find(eq("simulation_id", _id))
                                           .sort(ascending("_id"))
                                           .iterator();

        // Transform data for use with Phi_E Calculator.
        int column = 0;
        while (cursor.hasNext()) {
            Document d = cursor.next();
            ArrayList<Integer> array = (ArrayList) (d.get("data"));
            int[] vector = Ints.toArray(array);
            MatrixUtils.insertVectorIntoMatrix(vector, obs, column);
            column++;
        }

    }


    public static Document computePhiE(int[][] observations) {

        // Use tau = 1;
        int tau = 1;
        IntegratedInformationEmpiricalCalculatorDiscrete iicd;

        // Compute Phi_E and Minimium Information Partition.
        iicd = new IntegratedInformationEmpiricalCalculatorDiscrete(2, tau);
        iicd.addObservations(observations);
        iicd.computePossiblePartitions();
        double ii = iicd.compute();
        double mi = iicd.getMutualInformation();
        ArrayList<List<Integer>> mib = new ArrayList<List<Integer>>();
        mib.add(Ints.asList(iicd.minimumInformationPartition[0]));
        mib.add(Ints.asList(iicd.minimumInformationPartition[1]));

        // Put values in return document.
        Document doc = new Document();
        doc.put("phi_e", ii);
        doc.put("mib", mib);
        doc.put("tau", tau);
        doc.put("mi", mi);

        return doc;

    }

    public static Document computePhiETilde(int[][] observations) {

        // Use tau = 1;
        int tau = 1;
        IntegratedInformationEmpiricalTildeCalculatorDiscrete iicd;

        // Compute Phi_E and Minimium Information Partition.
        iicd = new IntegratedInformationEmpiricalTildeCalculatorDiscrete(2,
                                                                         tau);
        iicd.addObservations(observations);
        iicd.computePossiblePartitions();
        double ii = iicd.compute();
        ArrayList<List<Integer>> mib = new ArrayList<List<Integer>>();
        mib.add(Ints.asList(iicd.minimumInformationPartition[0]));
        mib.add(Ints.asList(iicd.minimumInformationPartition[1]));

        // Put values in return document.
        Document doc = new Document();
        doc.put("phi_e_tilde", ii);
        doc.put("mib_tilde", mib);

        return doc;

    }

    public static double computeHc(int[][] observations) {

        int base = 2;
        CoalitionEntropyCalculatorDiscrete cecd;
        cecd = new CoalitionEntropyCalculatorDiscrete(base);
        cecd.addObservations(observations);
        return cecd.compute();

    }


    public static void save(MongoCollection<Document> simulations,
                            ObjectId _id,
                            Document doc) {

        // Store results in MongoDB.
        Document setDoc = new Document();
        setDoc.put("$set", doc);
        simulations.updateOne(eq("_id", _id), setDoc);

    }

    public static void computePhiEForGeneratedData(boolean save) {

        // Collection Names.
        String simCollection = "generator_simulation";
        String dataCollection = "generator_data";

        // Query.
        Document query = new Document();
        Document ne = new Document("$exists", false);
        query.put("phi_e", ne);

        MongoDatabase db = connect();
        MongoCollection<Document> sims = db.getCollection(simCollection);
        MongoCollection<Document> data = db.getCollection(dataCollection);
        FindIterable<Document> results = sims.find(query);

        for (Document doc : results) {

            // Get ObjectId for simulation.
            ObjectId _id = doc.getObjectId("_id");
            int numVars = doc.getInteger("num_vars");
            int duration = doc.getInteger("duration");
            int[][] obs = new int[numVars][duration];
            getSimulationData(data, _id, obs);

            // Normal.
            Document values = computePhiE(obs);
            double hc = computeHc(obs);
            values.put("h_c", hc);
            if (save)  {
                save(sims, _id, values);
            }

            // Print results to console.
            System.out.println("Normal");
            System.out.println(values);
            System.out.println();

            // Shuffled.
            obs = MatrixUtils.shuffle(obs);
            values = computePhiE(obs);
            hc = computeHc(obs);
            values.put("h_c", hc);
            if (save)  {
                Document shuffled = new Document();
                shuffled.put("shuffled", values);
                save(sims, _id, shuffled);
            }

            // Print results to console.
            System.out.println("Shuffled");
            System.out.println(values);
            System.out.println();
        }

    }

    public static void computeNormalisedPhiEShuffled(boolean save) {

        // Collection Names.
        String simCollection = "oscillator_simulation";
        String dataCollection = "oscillator_data";

        // Query.
        Document query = new Document();
        Document ne = new Document("$exists", false);
        query.put("shuffled_normalised", ne);
        query.put("is_surrogate", false);

        MongoDatabase db = connect();
        MongoCollection<Document> sims = db.getCollection(simCollection);
        MongoCollection<Document> data = db.getCollection(dataCollection);
        FindIterable<Document> results = sims.find(query);

        for (Document doc : results) {

            // Get ObjectId for simulation.
            ObjectId _id = doc.getObjectId("_id");
            int numVars = doc.getInteger("num_oscillators");
            int duration = doc.getInteger("duration");
            int[][] obs = new int[numVars][duration];
            getSimulationData(data, _id, obs);

            // Compute.
            Document values = computePhiE(obs);
            if (save)  {
                Document shuffled = new Document();
                shuffled.put("shuffled_normalised", values);
                save(sims, _id, shuffled);
            }

        }

    }

    public static void computeSortedSurrogateDataAnalysis(boolean save) {

        // Collection Names.
        String simCollection = "oscillator_simulation";
        String dataCollection = "oscillator_data";

        // Query.
        Document query = new Document();
        Document ne = new Document("$exists", false);
        query.put("sorted", ne);
        query.put("is_surrogate", false);
        query.put("duration", 5000);
        query.put("num_oscillators", 8);

        MongoDatabase db = connect();
        MongoCollection<Document> sims = db.getCollection(simCollection);
        MongoCollection<Document> data = db.getCollection(dataCollection);
        FindIterable<Document> results = sims.find(query);

        for (Document doc : results) {

            // Get ObjectId for simulation.
            ObjectId _id = doc.getObjectId("_id");
            int numVars = doc.getInteger("num_oscillators");
            int duration = doc.getInteger("duration");
            int[][] obs = new int[numVars][duration];
            getSimulationData(data, _id, obs);

            // Compute sorted.
            System.out.println("Make sure to uncomment line in Input.java.");
            System.exit(1);
            Document values = computePhiE(obs);
            Document tilde = computePhiETilde(obs);

            double hc = computeHc(obs);
            double phi_e_tilde = tilde.getDouble("phi_e_tilde");
            values.put("coalition_entropy", hc);
            values.put("mib_tilde", tilde.get("mib_tilde"));
            values.put("phi_e_tilde", phi_e_tilde);
            System.out.println(phi_e_tilde);

            if (save)  {
                Document sorted = new Document();
                sorted.put("sorted", values);
                save(sims, _id, sorted);
            }
        }

    }

    public static void computeShuffledSurrogateDataAnalysis(boolean save) {

        // Collection Names.
        String simCollection = "oscillator_simulation";
        String dataCollection = "oscillator_data";

        // Query.
        Document query = new Document();
        Document ne = new Document("$exists", false);
        query.put("shuffled", ne);
        query.put("is_surrogate", false);
        query.put("duration", 5000);
        query.put("num_oscillators", 8);

        MongoDatabase db = connect();
        MongoCollection<Document> sims = db.getCollection(simCollection);
        MongoCollection<Document> data = db.getCollection(dataCollection);
        FindIterable<Document> results = sims.find(query);

        for (Document doc : results) {

            // Get ObjectId for simulation.
            ObjectId _id = doc.getObjectId("_id");
            int numVars = doc.getInteger("num_oscillators");
            int duration = doc.getInteger("duration");
            int[][] obs = new int[numVars][duration];
            getSimulationData(data, _id, obs);

            // Compute shuffled.
            obs = MatrixUtils.shuffle(obs);
            Document values = computePhiE(obs);
            Document tilde = computePhiETilde(obs);
            double hc = computeHc(obs);
            double phi_e_tilde = tilde.getDouble("phi_e_tilde");
            values.put("coalition_entropy", hc);
            values.put("mib_tilde", tilde.get("mib_tilde"));
            values.put("phi_e_tilde", phi_e_tilde);

            if (save)  {
                Document shuffled = new Document();
                shuffled.put("shuffled", values);
                save(sims, _id, shuffled);
            }

        }

    }

    public static void main(String[] args) {

        System.out.println("Start tests.");
        testMutualInformation();
        testMutualInformationTimeSeries();
        testMutualInformationTimeSeriesPairs();
        testIntegratedInformation();
        testCoalitionEntropy();
        System.out.println("Tests completed.");

        computePhiEForGeneratedData(false);
        computeNormalisedPhiEShuffled(false);
        computeCoalitionEntropy(false);

        // Compute phi at various values of tau.
        computeIntegratedInformation("kuramoto", 1, false, false, true);
        computeIntegratedInformation("kuramoto", 5, false, false, true);
        computeIntegratedInformation("kuramoto", 10, false, false, true);
        computeIntegratedInformation("kuramoto", 15, false, false, true);
        computeIntegratedInformation("kuramoto", 20, false, false, true);

        computeSortedSurrogateDataAnalysis(false);
        computeShuffledSurrogateDataAnalysis(false);
    }

}
