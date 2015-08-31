package com.company;

import infodynamics.measures.discrete.EntropyCalculatorDiscrete;
import infodynamics.utils.MathsUtils;
import infodynamics.utils.MatrixUtils;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by juancarlosfarah on 22/05/15.
 *
 */
public class IntegratedInformationEmpiricalCalculatorDiscrete {

    private int base;
    private int tau;
    private int[][] data;
    public Set<int[]> partitions;
    public int[][] minimumInformationPartition;
    private double minimumInformationPartitionValue;
    private double mutualInformation;


    public IntegratedInformationEmpiricalCalculatorDiscrete(int base, int tau) {
        this.base = base;
        this.tau = tau;
        partitions = new HashSet<int[]>();
        minimumInformationPartition = new int[2][];
        minimumInformationPartitionValue = Double.POSITIVE_INFINITY;
    }

    public void addObservations(int[][] data) {
        this.data = data;
    }

    public void computePossiblePartitions() {
        try {

            for (int i = 1; i < data.length; i++) {
                int[][] sets = MathsUtils.generateAllSets(data.length, i);
                partitions.addAll(Arrays.asList(sets));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public double compute() {

        double integratedInformation = 0.0;
        EffectiveInformationCalculatorDiscrete eicd;
        eicd = new EffectiveInformationCalculatorDiscrete(base, tau);
        eicd.addObservations(data);
        mutualInformation = eicd.computeMutualInformationForSystem();

        for (int[] partition : partitions) {

            double k = computeNormalizationFactor(partition);
            double ei = eicd.computeForBipartition(partition);

            // If k = 0, it means that one of the partitions has an entropy
            // of 0, which means that it doesn't tell us anything about the
            // rest of the system. Return 0 otherwise return normalised EI.
            double mipScore = (k == 0) ? 0 : ei / k;

            if (mipScore < minimumInformationPartitionValue) {
                minimumInformationPartition[0] = partition;
                int[] partition2 = new int[data.length - partition.length];
                int index = 0;
                for (int i = 0; i < data.length; i++) {
                    if (!MatrixUtils.contains(partition, i)) {
                        partition2[index] = i;
                        index++;
                    }
                }
                minimumInformationPartition[1] = partition2;
                minimumInformationPartitionValue = mipScore;
                integratedInformation = ei;
            }

        }
        return integratedInformation;
    }

    public double computeNormalizationFactor(int[] partition) {

        int[][] part1 = MatrixUtils.selectRows(this.data, partition);
        int[][] part2 = MatrixUtils.selectAllRowsExcept(this.data, partition);

        return computeNormalizationFactor(part1, part2);
    }


    public double computeNormalizationFactor(int[][] part1, int[][] part2) {

        EntropyCalculatorDiscrete ecd = new EntropyCalculatorDiscrete(base);
        ecd.initialise();
        ecd.addObservations(part1);
        double entropy1 = ecd.computeAverageLocalOfObservations();

        ecd.initialise();
        ecd.addObservations(part2);
        double entropy2 = ecd.computeAverageLocalOfObservations();

        return Math.min(entropy1, entropy2);

    }

    public double getMutualInformation() {
        return mutualInformation;
    }

}
