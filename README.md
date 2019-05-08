Guided Mode Resonance structure analysis
==========================

*Version 0.1*

A set of scripts, packaged for use by the [Photonics Research Group](https://www.york.ac.uk/physics/photonics) at the [Department of Physics,](https://www.york.ac.uk/physics)[University of York](https://www.york.ac.uk), for
analysis of the data generated by their in-house guided mode resonance
microscopes.

Features
--------

The seven modules included in this package do the following:

* read in experimental configuration files
* load the generated CSV files
* normalise the CSV data to incident source intensity
* export normalised data as ndarray (for quicker loading)
* Analyse the data:
  * Free-spectral-range
    * take spectral data per pixel and calculate FSR for sample at
      that point
    * calculate pixel by pixel refractive index of sample
    * produce / export refractive index image
  * Simple maximum  (TO BE IMPLEMENTED)
    * take spectral data and find maximum value - corresponding to resonant
      wavelength
  * Fano fitting (TO BE IMPLEMENTED)
    * fit a Fano shape to the spectral data to find resonant wavelength
  * Differential Fano fit (TO BE IMPLEMENTED)
    * differentiate spectral data and fit differential Fano, less error
      prone than direct fit
  * Multiple Fano / differential Fano fit (TO BE IMPLEMENTED)

This package was developed within the [Photonics Research Group](https://www.york.ac.uk/physics/photonics), based at the [Department of Physics,](https://www.york.ac.uk/physics) [Univeristy of York](https://www.york.ac.uk).

Requirements and installation
-----------------------------

This package has been tested with Python 3.7; use with earlier versions of
Python is at your own risk.

This package is primarily for use by the Photonics Research Group, it is
designed specifically for our experimental set-ups, however, feel free to
look into how we do our data analysis and please suggest improvements -
none of the "developers" here are full time coders!