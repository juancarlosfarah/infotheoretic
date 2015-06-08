package com.company;

import com.google.common.primitives.Ints;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.util.JSON;
import infodynamics.measures.discrete.MutualInformationCalculatorDiscrete;
import infodynamics.utils.MatrixUtils;
import infodynamics.utils.RandomGenerator;
import org.bson.Document;
import org.bson.types.ObjectId;

import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Sorts.ascending;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {

    public static MongoDatabase connect(String host,
                                        int port,
                                        String database) {

        MongoClient mongoClient = new MongoClient(host , port);

        return mongoClient.getDatabase(database);
    }


    public static void testMutualInformation() {

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

    }

    public static void testMutualInformationTimeSeries() {
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

    }

    public static void testMutualInformationTimeSeriesPairs() {
        int[] var0 = { 0, 0, 0, 0, 0, 1, 1, 0};
        int[] var1 = { 1, 1, 1, 0, 0, 1, 1, 0};
        int[] var2 = { 1, 1, 1, 0, 0, 1, 0, 0};
        int[] var3 = { 0, 0, 1, 0, 1, 1, 1, 0};
        int[] var4 = { 1, 1, 1, 0, 1, 0, 1, 1};
        int[] var5 = { 0, 0, 1, 0, 1, 1, 1, 0};

        int[][] states = { var0, var1, var2, var3, var4, var5 };

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

    }

    public static void main(String[] args) {

        System.out.println("Running tests...");
        testMutualInformation();
        System.out.println("\n");

        testMutualInformationTimeSeries();
        System.out.println("\n");

        System.out.println("Testing MI on time series pairs...");
        testMutualInformationTimeSeriesPairs();
        System.out.println("\n");

        // Use tau = 1;
        int tau = 1;

        System.out.println("First Effective Information Test:");

        int[] var0 = {0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0};
        int[] var1 = {0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1};

        RandomGenerator rg = new RandomGenerator();
        int[] var0a = rg.generateRandomInts(1000000, 2);
        var0a[0] = 0;
        int[] var1a = new int[1000000];
        var1a[0] = 0;
        for (int i = 1; i < 1000000; i++) {
            var1a[i] = var0a[i - 1];
        }

        int[][] states0 = {var0a, var1a};

        EffectiveInformationCalculatorDiscrete eicd;
        eicd = new EffectiveInformationCalculatorDiscrete(2, tau);
        eicd.addObservations(states0);

        int[] p0 = {0};
        double o0 = eicd.computeForBipartition(p0);
        System.out.println(o0);

        int[] p1 = {1};
        double o1 = eicd.computeForBipartition(p1);
        System.out.println(o1);

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

        IntegratedInformationCalculatorDiscrete iicd;
        iicd = new IntegratedInformationCalculatorDiscrete(2, tau);
        iicd.addObservations(states1);
        iicd.computePossiblePartitions();

        // System.out.println("\n");
        // System.out.println("Printing possible partitions:");
        // for (int[] set : iicd.partitions) {
        //    System.out.println(Arrays.toString(set));
        // }

        System.out.println(iicd.compute());
        System.out.println(Arrays.deepToString(iicd.minimumInformationPartition));

        System.out.println("\n");
        System.out.println("Second Integrated Information Test:");

        int[][] states2 = rg.generateRandomInts(8, 10000, 2);

        iicd = new IntegratedInformationCalculatorDiscrete(2, tau);
        iicd.addObservations(states2);
        iicd.computePossiblePartitions();
        System.out.println(iicd.compute());
        System.out.println(Arrays.deepToString(iicd.minimumInformationPartition));

        // Test with data from Kuramoto Oscillator simulations.
        MongoDatabase db = connect("localhost", 27017, "individual_project");
        MongoCollection<Document> simulation;
        MongoCollection<Document> data;
        simulation = db.getCollection("oscillator_simulation");
        data = db.getCollection("oscillator_data");

        Document ne = new Document("$exists", false);
        Document query = new Document("integrated_information_e", ne);

        MongoCursor<Document> c = simulation.find(query).iterator();

        while (c.hasNext()) {

            Document doc = c.next();

            // Get ObjectId for simulation.
            ObjectId _id = doc.getObjectId("_id");

            // Get data for this simulation.
            MongoCursor<Document> cursor = data.find(eq("simulation_id", _id))
                    .sort(ascending("_id"))
                    .iterator();

            int num_oscillators = doc.getInteger("num_oscillators");
            int duration = doc.getInteger("duration");

            int[][] obs = new int[num_oscillators][duration];

            int column = 0;
            while (cursor.hasNext()){
                Document d = cursor.next();
                ArrayList<Integer> array = (ArrayList)(d.get("data"));
                int[] vector = Ints.toArray(array);
                MatrixUtils.insertVectorIntoMatrix(vector, obs, column);
                column++;
            }

            iicd = new IntegratedInformationCalculatorDiscrete(2, tau);
            iicd.addObservations(obs);
            iicd.computePossiblePartitions();
            double ii = iicd.compute();
            ArrayList<List<Integer>> mib = new ArrayList<List<Integer>>();

            mib.add(Ints.asList(iicd.minimumInformationPartition[0]));
            mib.add(Ints.asList(iicd.minimumInformationPartition[1]));

            Document update = new Document();
            update.put("integrated_information_e", ii);
            update.put("min_information_bipartition", mib);
            update.put("tau", tau);
            Document setDoc = new Document("$set", update);
            simulation.updateOne(eq("_id", _id), setDoc);
        }

    }
}
