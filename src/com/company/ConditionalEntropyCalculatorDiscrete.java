package com.company;

import infodynamics.measures.discrete.EntropyCalculatorDiscrete;
import infodynamics.measures.discrete.MutualInformationCalculatorDiscrete;

/**
 * Created by juancarlosfarah on 16/06/15.
 *
 */
public class ConditionalEntropyCalculatorDiscrete {

    MutualInformationCalculatorDiscrete micd;
    EntropyCalculatorDiscrete ecd;
    int base;

    public ConditionalEntropyCalculatorDiscrete(int base) {
        this.base = base;

        try {
            micd = new MutualInformationCalculatorDiscrete(base, 0);
            ecd = new EntropyCalculatorDiscrete(base);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void addObservations(int[] var1, int[] var2) {

        // Initialise.
        micd.initialise();
        ecd.initialise();

        // Add observations.
        micd.addObservations(var1, var2);
        ecd.addObservations(var1);

    }

    public double compute() {

        double mi = micd.computeAverageLocalOfObservations();
        double h = ecd.computeAverageLocalOfObservations();

        return h - mi;
    }
}
