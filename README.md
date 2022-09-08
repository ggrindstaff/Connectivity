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
* landscape_clip_AOIs: csv files with elevation data for a set of DTM clips containing berms and/or stock ponds
   * AOI1_stockpond_clip.csv
   * AOI2_berms_clip.csv
   * AOI2_stockpond_clip.csv
   * AOI3_berms_clip.csv
   * AOI3_stockpond_clip2.csv
   * AOI4_berms_clip.csv
   * AOI5_berms_clip.csv
* Berms: unaltered landscape clips with paired DTMs with synthetically added berms
   * OBJ2
      * DEM
         * AOI_OBJ2_untreated.csv: original DTM
         * AOI_OBJ2_untreated_AddedStruct.csv: with added berms
   * OBJ4
      * DEM
         * AOI_OBJ4_untreated.csv: original DTM
         * AOI_OBJ4_untreated_AddedStruct.csv: with added berms
* Colab_notebooks: Code for apply persistence homology to synthetic examples and DTMs
   * PH_Examples.ipynb: persistence homology applied to examples in directory Synthetics
   * Synthetic_BERM_PlottingCycles.ipynb: application of persistence homology to paired unaltered landscapes and DTMs with synthetically added berms
   * earthwork_detection_PlottingCycles.ipynb: application of persistence homology to small DTM clips containing berms and stock ponds
   * Copy_of_BERM_PlottingCycles1.ipynb: application of persistence to a larger DTM in the Altar Valley, AZ
