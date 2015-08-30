package com.company;

import infodynamics.utils.MatrixUtils;

import java.util.Arrays;
import java.util.HashMap;

/**
 * Created by juancarlosfarah on 26/05/15.
 *
 */
public class Input {

    private int[][] original;
    private int base;
    private int[] reduced;
    private int reducedBase;
    private HashMap<Integer, Integer> map;
    private int[][] paired;

    public Input(int[][] data, int base) {
        this.original = data;
        this.base = base;
        this.map = new HashMap<Integer, Integer>();
        this.paired = new int[2][];
        reduce();

    }

    public HashMap<Integer, Integer> reduce() {

        try {
            int[][] t = MatrixUtils.transpose(original);
            this.reduced = MatrixUtils.computeCombinedValues(t, base);

            // Uncomment if you need to sort.
//            Arrays.sort(this.reduced);

            // Reduced base will equal the original base
            // to the power of the number of variables.
            reducedBase = (int)(Math.pow(base, original.length));

        } catch (Exception e) {
            e.printStackTrace();
        }

        return map;
    }

    public int[][] pair(int tau) {
        paired[0] = Arrays.copyOfRange(reduced, 0, reduced.length - tau);
        paired[1] = Arrays.copyOfRange(reduced, tau, reduced.length);

        return paired;
    }

    public int getReducedBase() {
        return reducedBase;
    }

    @Override
    public String toString() {
        return "Input{" +
                "original=" + Arrays.deepToString(original) +
                ", base=" + base +
                ", reduced=" + Arrays.toString(reduced) +
                ", reducedBase=" + reducedBase +
                ", map=" + map +
                ", paired=" + Arrays.deepToString(paired) +
                '}';
    }
}
