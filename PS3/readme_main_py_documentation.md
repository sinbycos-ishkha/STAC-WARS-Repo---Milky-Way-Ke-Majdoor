# STAC WARS - PS 3: EXOPLANET HUNTERS
## Computational Solution (`main.py`)

This repository contains the `main.py` Python script designed to automate the analysis of stellar brightness data to detect and classify exoplanets, as outlined in the "Operation Dim Star" mission brief.

### 🚀 Overview
The script mathematically processes light-curve observations for three stars (STAC-1, STAC-2, and STAC-3). It calculates transit depths, planetary radii, and orbital distances, ultimately outputting a formatted scientific report in the terminal.

### ⚙️ Requirements
* **Python 3.x**
* No external dependencies or pip installs are required. The script relies entirely on standard built-in Python libraries: `csv`, `math`, and `os`.

### 📂 How to Use
1. Place `main.py` in your working directory.
2. (Optional) Place the CSV data files in a `/csv/` subfolder. If the script cannot find the CSVs, it will automatically fall back to the built-in hardcoded data arrays.
3. Open your terminal or command prompt.
4. Run the script using the following command:
   ```bash
   python main.py
   ```
5. Review the comprehensive console output which acts as the final report.

### 🏗️ Code Architecture
The code is divided into four main functional blocks:

1. **Constants & Stellar Properties:**
   * Defines astronomical constants (e.g., Solar Radius, Earth Radius, AU in km).
   * Stores host star parameters (Mass, Radius, Luminosity, Temp) in a structured dictionary `STELLAR_PROPERTIES`.
   * Contains the `FALLBACK_OBSERVATIONS` array to ensure the code runs flawlessly even without external CSV files.

2. **Helper Functions:**
   * `load_observations(star_name)`: Intelligently routes data loading from either a CSV or the fallback dictionaries.
   * `classify_planet(radius_earths)`: Uses `if/elif` logic to categorize the planet (Earth-sized, Super-Earth, Neptune-sized, Jupiter-sized) based on the calculated radius.

3. **Analysis Pipeline (`analyse_system`):**
   * **Part A (Detection):** Finds baseline brightness ($F_{normal}$) and calculates transit depth ($\delta$). 
   * **Part B (Size):** Uses the equation $R_p = R_s \sqrt{\delta}$ to find the planetary radius.
   * **Part C (Orbits):** Checks if consecutive transit gaps are strictly equal. If they are, it calculates the orbit using Kepler's Third Law: $P^2 = a^3 / M$.
   * **Part D (Habitable Zone):** Calculates the ideal habitable zone center using $d_{HZ} \approx \sqrt{L/L_\odot}$.

4. **Execution & Report (`main`):**
   * Iterates through all three star systems, passes them through the analysis pipeline, and dynamically prints a highly formatted, step-by-step console report mimicking the required mission submission.

### ⚠️ Important Assumptions & Limitations
* **Strict Periodicity Rule:** The script is programmed with a rigid condition: it will only calculate an orbital period if *all consecutive transit gaps are perfectly equal*. 
* Because STAC-3 has mixed gaps (indicating a multi-planet system), the script flags its period as "Undetermined" and defaults to recommending STAC-2. Analysts should manually review STAC-3's light curve for overlapping planetary transits!