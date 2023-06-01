# Connectivity

This repository contains code for automatic detection of berms and stockponds, and figures accompanying the paper *Automated earthwork detection using topological
persistence*, by Dana A Lapides, Gillian Grindstaff, and Mary H Nichols. 

Contents of repository:
* Synthetics: csv files with elevation data for simple example landscapes
    * example 1: flat slope
    * example 2: slope with random noise
    * example 3: slope with a straight channel
    * example 4: slope with a branched channel
    * example 5: square pit
    * example 6: slope with contour berm
* landscape_clip_AOIs: csv file with elevation data for a DTM clip containing a stock pond
   * AOI1_stockpond_clip.csv
* Berms: unaltered landscape clips with paired DTMs with synthetically added berms
   * berm_characteristics - Sheet1.csv: csv containing data about berms detected and not detected with persistence in this study
   * OBJ2
      * DEM
         * AOI_OBJ2_untreated.csv: original DTM
         * AOI_OBJ2_untreated_AddedStruct.csv: with added berms
         * AOI_OBJ2_Case1Taper_converted.csv: with tapered berms
         * AOI_OBJ2_Case2Breach_converted.csv: with breached berms
         * AOI_OBJ2_untreated_AddedStruct_Case3Terrace.csv: with sedimented berms
   * OBJ4
      * DEM
         * AOI_OBJ4_untreated.csv: original DTM
         * AOI_OBJ4_untreated_AddedStruct.csv: with added berms
         * AOI_OBJ4_Case1Taper_converted.csv: with tapered berms
         * AOI_OBJ4_Case2Breach_converted.csv: with breached berms
         * AOI_OBJ4_untreated_AddedStruct_Case3Terrace.csv: with sedimented berms
* Colab_notebooks: Code for applying persistence homology to synthetic examples and DTMs
   * PH_Examples.ipynb: persistence homology applied to examples in directory Synthetics
   * Synthetic_BERM_PlottingCycles.ipynb: application of persistence homology to paired unaltered landscapes and DTMs with synthetically added berms of four different types for 2 sites
   * 4sites_berm_detection.ipynb: application of persistence homology to four sites in Arizona to identify berms
   * berm_id_exploration.ipynb: a notebook looking at data collected on berms identified in 4sites_berm_detection.ipynb
   * stockpond_detection_example.ipynb: application of persistence homology to small DTM clip containing a stock pond
* griddemofig.py: code to generate schematic figure of how persistence works
