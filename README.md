# DAC_Cost_Model

## Description
Accompanying code for "Considering technology characteristics to project future costs of direct air capture".

You can cite all versions by using the DOI 10.5281/zenodo.10617769. This DOI represents all versions, and will always resolve to the latest one.

### Dependencies
The following are required to run the code: 
- Python 3.8 or higher
- numpy
- pandas
- [XlsxWriter](https://xlsxwriter.readthedocs.io/index.html)

### Installing
You can clone the repository and run the code locally using the CLI or a Python IDE. To install all dependencies, run the following command in the terminal:
```bash
pip install -r requirements.txt
```

#### Running the Application
The two main ways to run the program are: 
1. `main_monte_carlo.py` - runs the Monte Carlo simulation
2. `main_sensitivity_analysis.py` - runs the sensitivity analysis

## Authors and correspondence
Katrin Sievert - katrin.sievert@gess.ethz.ch

## License
The details of the license can be found in the [LICENSE](https://github.com/kfdsievert/Cost-Model--DAC/blob/main/LICENSE) file.

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## Important 
- The code runs Monte Carlo simulations that may require significant processing time.
- The code creates an output folder in the directory where it is run. All outputs are stored here.
