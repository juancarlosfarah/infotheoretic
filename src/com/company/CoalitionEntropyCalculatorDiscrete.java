package com.company;

import infodynamics.utils.MatrixUtils;

import java.util.*;

/**
 * Calculates coalition entropy for system.
 * Created by juancarlosfarah on 15/06/15.
 */
public class CoalitionEntropyCalculatorDiscrete {
    int[] data;
    int base;
    int num_coalitions;
    double value;
    public Map<Integer, Integer> coalitionCountMap;

    public CoalitionEntropyCalculatorDiscrete(int base) {
        this.base = base;
        coalitionCountMap = new HashMap<Integer, Integer>();
    }

    public void addObservations(int[][] states) {
        num_coalitions = (int) Math.pow(2, states.length);
        int[][] states_t = MatrixUtils.transpose(states);
        try {
            data = MatrixUtils.computeCombinedValues(states_t, base);

            // Initialise coalition count map.
            for (int i = 0; i < num_coalitions; i++) {
                coalitionCountMap.put(i, 0);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public double compute() {

        double rvalue;
        double sum = 0;

        for (int state : data) {

            // Increase count for this coalition.
            Integer count = coalitionCountMap.get(state);
            count++;
            coalitionCountMap.put(state, count);

        }

        Iterator<Map.Entry<Integer, Integer>> it;
        it = coalitionCountMap.entrySet().iterator();

        while (it.hasNext()) {
            double value;
            Map.Entry<Integer, Integer> pair = it.next();
            value = pair.getValue();
            value /= data.length;

            // Make log(0) equal to 0.
            double log = (value == 0) ? 0 : Math.log(value);

            // Use division rule to get log base 2.
            sum += value * (log / Math.log(2));
        }

        rvalue = -(1 / (Math.log(num_coalitions) / Math.log(2))) * sum;

        // Store the value in object property.
        this.value = rvalue;

        return rvalue;

    }

    @Override
    public String toString() {
        return "CoalitionEntropyCalculatorDiscrete{" +
                "data=" + Arrays.toString(data) +
                ", base=" + base +
                ", num_coalitions=" + num_coalitions +
                ", coalitionCountMap=" + coalitionCountMap +
                '}';
    }
}
