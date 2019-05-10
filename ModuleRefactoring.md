Module Refactoring Requirements
===============================

This document outlines the steps involved in analysing GMR data produced
by our in-house GMR microscopes.  The steps are then outlined as potential
packages, modules and functions below.  At the bottome is a simple TODO list
please amend as appropriate.

Steps required for data analysis
--------------------------------

1. locate images
   * have user put files in one location (default: local folder)
   * optionally have user enter files location (could be NAS)
2. load experimental settings
   * set-up analysis variables
     * directories (create new if required)
     * filenames
     * wavelength start, finish, step
     * time step
3. load images, save out as numpy arrays
   1. calculate approximate time / memory requirements - report to user
   2. allow user to safely stop or continue script
      * do they want to load / save to NAS (cost: time)
      * do they want to show images (cost: time)
      * do they want to save images (cost: time, memory)
   3. prepare data (default: from power meter)
      1. load numpy arrays
      2. prepare data
         * normalise
           * from power meter readings
           * from image background
           * ...
         * slice data
           * filter spectral information (number of files to load)
           * filter time information (number of folders to read)
           * filter spatial information (slice numpy array)
         * transpose data
           * take rows of each numpy array (vectors) and construct 2D array
      3. save prepared data as numpy arrays
4. analyse data
   1. load numpy arrays
   2. analyse data
      * find resonance
        * simply max search
        * simple Fano fit
        * double Fano fit
        * differential Fano fit
        * differential double Fano fit
        * phase analysis (Isabel, Kezheng)
        * ...
   3. output analysis
      * save plot
      * show plot to user (cost: time)

Module requirements
-------------------

1. InputOutput  << import GMR.InputOutput as io >>
   * load experimental settings  ( io.exp_in() )
   * load raw image data  ( io.raw_in() )
   * load numpy arrays  ( io.array_in() )
   * save numpy arrays  ( io.data_array_out() )
   * save pngs  ( io.png_out() )
   * save csvs  ( io.csv_out() )
   * request input from user  ( io.user_in() )
2. DataPreparation  << import GMR.DataPreparation as dp >>
   * power meter normalise ( dp.pwr_norm() )
   * BG normalise  ( dp.bg_norm() )
   * trim spectrum  ( dp.trim_spec() )
   * trim time series  ( dp.trim_time() )
   * ROI (trim spatial data)  ( dp.roi() )
   * transpose  ( dp.trans() )
3. DataAnalysis  << import GMR.DataAnalysis as da >>
   * find resonance  << da.Resonance.simple() >>
     * simple analysis  ( da.resonance.simple() )
        * maximum / minimum  
          * thresholds
        * average
        * standard deviation
     * single Fano  ( da.resonance.s_fano() )
     * double Fano  ( da.resonance.d_fano() )
     * single differential Fano  ( da.resonance.sd_fano() )
     * double differential Fano  ( da.resonacne.dd_fano() )
   * find refractive index  << da.RIndex.toFreq() >>
     * convert data to frequency  ( da.RIndex.toFreq() )
       * interpolate data for even spacing in frequency
     * find peaks (wavelength, frequency)  ( da.RIndex.peaks() )
       * threshold
     * calculate index from FSR  ( da.RIndex.fsr() )
4. Plotting (??) << import GMR.Plotting as p >>
   * Display single plot  ( p.s_plot() )
   * Display double plot  ( p.d_plot() )
   * Display image  ( p.im_plot() )

TODO
-----

* Move / add / subtract / rename functions