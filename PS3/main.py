"""STAC WARS - PS 3: EXOPLANET HUNTERS
Operation Dim Star: Find the Rebellion a New Home
=================================================
Complete computational solution for Parts A, B, C, and D based on PS3_Astronomy.pdf.

Questions Addressed:
Part A - Detect the Exoplanets:
    1. Determine whether observations indicate a transiting exoplanet.
    2. Determine orbital period (strictly checking if consecutive transit gaps are equal).
    3. Determine transit depth (delta = (Fnormal - Ftransit) / Fnormal).
    4. Physical explanation of periodic transit dips.

Part B - Determine Planet Size:
    5. Calculate planet radius in kilometres (Rp = Rs * sqrt(delta)).
    6. Express planet radius in terms of Earth radii (Rp / R_Earth).
    7. Classify planet size (Earth-sized, Super-Earth, Neptune-sized, Jupiter-sized).

Part C - Determine Planetary Orbits:
    8. Calculate orbital distance in AU using Kepler's 3rd Law (a = (P^2 * M)^(1/3)).
    9. Convert orbital distance into kilometres (1 AU = 149.6 million km).
    10. Compare orbital distance with Earth's distance from the Sun (1 AU).

Part D - Find the Most Promising World:
    11. Determine the most promising candidate for further habitability studies.
    12. Provide at least three pieces of evidence supporting the selection.
    13. Suggest an additional astronomical observation (Transmission Spectroscopy).

Submission Checklist:
    14. Detection & identification of exoplanets (Part A).
    15. Calculations of planetary radii (Part B).
    16. Calculations of orbital distances (Part C).
    17. Comparison of detected planets & candidate selection (Part D).
    18. Clear reasoning, formulas, and stated assumptions.
"""

import csv
import math
import os

# ==============================================================================
# 1. CONSTANTS & STELLAR PROPERTIES (From PS3_Astronomy.pdf)
# ==============================================================================
SOLAR_RADIUS_KM = 696000.0          # R_sun in km
EARTH_RADIUS_KM = 6371.0            # R_earth in km
AU_KM = 149600000.0                 # 1 AU in km (149.6 million km)
DAYS_PER_YEAR = 365.25              # 1 year in days

# Stellar parameters from Section 1 (Table 1, Page 4)
STELLAR_PROPERTIES = {
    "STAC-1": {
        "mass": 1.00,               # M_sun
        "radius": 1.00,             # R_sun
        "luminosity": 1.00,         # L_sun
        "surface_temp_k": 5800,     # K
        "spectral_type": "G-type (Solar-like)",
    },
    "STAC-2": {
        "mass": 0.80,               # M_sun
        "radius": 0.80,             # R_sun
        "luminosity": 0.40,         # L_sun
        "surface_temp_k": 5000,     # K
        "spectral_type": "K-type (Orange Dwarf)",
    },
    "STAC-3": {
        "mass": 0.50,               # M_sun
        "radius": 0.50,             # R_sun
        "luminosity": 0.08,         # L_sun
        "surface_temp_k": 3800,     # K
        "spectral_type": "M-type (Red Dwarf)",
    },
}

# CSV data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILES = {
    "STAC-1": os.path.join(BASE_DIR, "csv", "STAC-1_Brightness_Data.csv"),
    "STAC-2": os.path.join(BASE_DIR, "csv", "STAC-2_Brightness_Data.csv"),
    "STAC-3": os.path.join(BASE_DIR, "csv", "STAC-3_Brightness_Data.csv"),
}

# Fallback observational data exactly as presented in PS3_Astronomy.pdf
FALLBACK_OBSERVATIONS = {
    "STAC-1": [
        (0, 1.0000), (1, 1.0000), (2, 1.0000), (3, 0.9970), (4, 1.0000),
        (5, 1.0000), (6, 1.0000), (7, 1.0000), (8, 0.9970), (9, 1.0000),
        (10, 1.0000), (11, 1.0000), (12, 0.9970), (13, 1.0000), (14, 1.0000),
        (15, 1.0000), (16, 0.9970), (17, 1.0000), (18, 1.0000), (19, 1.0000),
        (20, 0.9970),
    ],
    "STAC-2": [
        (0, 1.0000), (20, 0.9990), (40, 1.0000), (60, 1.0000), (80, 1.0000),
        (100, 0.9990), (120, 1.0000), (140, 1.0000), (160, 1.0000), (180, 0.9990),
        (200, 1.0000),
    ],
    "STAC-3": [
        (0, 1.0000), (10, 1.0000), (20, 0.9990), (30, 1.0000), (40, 1.0000),
        (50, 1.0000), (60, 0.9992), (70, 1.0000), (80, 1.0000), (90, 1.0000),
        (100, 0.9991), (110, 1.0000), (120, 1.0000), (130, 1.0000), (140, 0.9993),
        (150, 1.0000), (160, 1.0000), (170, 0.9990), (180, 1.0000), (190, 1.0000),
        (200, 1.0000),
    ],
}


# ==============================================================================
# 2. HELPER FUNCTIONS
# ==============================================================================
def load_observations(star_name):
    """
    Load observation times and relative brightness.
    Checks for the CSV file first; if the CSV file or folder is not present,
    it automatically falls back to the built-in observations from PS3_Astronomy.pdf.
    Can run 100% independently with ZERO external data files or libraries.
    """
    file_path = DATA_FILES.get(star_name)
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [
                    (float(row["Time (days)"]), float(row["Rel. brightness"]))
                    for row in reader
                ]
        except Exception:
            pass
    return FALLBACK_OBSERVATIONS[star_name]


def classify_planet(radius_earths):
    """
    Classify and tag exoplanet into one of the four categories specified in PDF Question 7:
      - 'Earth-sized'   : Rp <= 1.25 Earth radii (terrestrial rocky planets)
      - 'Super-Earth'   : 1.25 < Rp <= 2.0 Earth radii (large rocky / ocean worlds)
      - 'Neptune-sized' : 2.0 < Rp <= 6.0 Earth radii (ice giants / sub-Neptunes)
      - 'Jupiter-sized' : Rp > 6.0 Earth radii (gas giants)
    """
    if radius_earths <= 1.25:
        return "Earth-sized"
    elif radius_earths <= 2.0:
        return "Super-Earth"
    elif radius_earths <= 6.0:
        return "Neptune-sized"
    else:
        return "Jupiter-sized"


# ==============================================================================
# 3. ANALYSIS PIPELINE (PARTS A - D)
# ==============================================================================
def analyse_system(star_name):
    """
    Performs complete transit analysis for a given stellar system:
      - Identifies normal and minimum brightness
      - Detects transit events
      - Evaluates periodicity under the condition:
        'If the difference between any two consecutive values is not same,
         then do not find period for STAC. Find it if that is same.'
      - Calculates planet size (Part B)
      - Calculates orbital properties if periodic (Part C)
      - Computes habitable zone and compares candidate distance (Part D)
    """
    obs = load_observations(star_name)
    times = [t for t, b in obs]
    brightness = [b for t, b in obs]

    normal_brightness = max(brightness)
    minimum_brightness = min(brightness)

    # Part A, Question 1: Detect dips below baseline brightness
    transit_events = [(t, b) for t, b in obs if b < normal_brightness]
    transit_days = [t for t, b in transit_events]
    has_dips = len(transit_days) >= 2

    # Part A, Question 3: Transit depth delta = (Fnormal - Ftransit) / Fnormal
    transit_depth = (normal_brightness - minimum_brightness) / normal_brightness

    # Part A, Question 2: Consecutive transit interval analysis
    intervals = [
        t2 - t1 for t1, t2 in zip(transit_days, transit_days[1:])
    ]
    # Check whether all consecutive intervals are strictly equal
    all_intervals_equal = (len(set(intervals)) == 1) if intervals else False

    if all_intervals_equal:
        period_days = float(intervals[0])
    else:
        # User condition: if difference between any two consecutive values is not same,
        # then do not find period for STAC.
        period_days = None

    # Part B: Planet Size Calculation
    # Physical relation: delta = (Rp / Rs)^2 => Rp = Rs * sqrt(delta)
    # (Note: PDF formula box has typographic inversion delta ≈ (Rs/Rp)^2;
    #  physically sound cross-sectional area ratio is delta = (Rp/Rs)^2).
    star = STELLAR_PROPERTIES[star_name]
    star_radius_km = star["radius"] * SOLAR_RADIUS_KM
    planet_radius_km = star_radius_km * math.sqrt(transit_depth)
    planet_radius_earths = planet_radius_km / EARTH_RADIUS_KM
    planet_class = classify_planet(planet_radius_earths)

    # Part D: Habitable Zone center: dHZ = sqrt(L / L_sun) AU
    habitable_zone_au = math.sqrt(star["luminosity"])

    # Part C: Planetary Orbit using Kepler's Third Law (P^2 = a^3 / M)
    # a = (P^2 * M)^(1/3) where P is in years, M in solar masses, a in AU
    if period_days is not None:
        period_years = period_days / DAYS_PER_YEAR
        orbital_distance_au = (period_years**2 * star["mass"]) ** (1.0 / 3.0)
        orbital_distance_km = orbital_distance_au * AU_KM
        distance_from_hz_au = abs(orbital_distance_au - habitable_zone_au)
    else:
        orbital_distance_au = None
        orbital_distance_km = None
        distance_from_hz_au = None

    # Estimate approximate period if mode interval was used (for sensitivity notes)
    approx_period = max(set(intervals), key=intervals.count) if intervals else None

    planet_tag = classify_planet(planet_radius_earths)

    return {
        "star_name": star_name,
        "star_properties": star,
        "normal_brightness": normal_brightness,
        "minimum_brightness": minimum_brightness,
        "transit_days": transit_days,
        "intervals": intervals,
        "all_intervals_equal": all_intervals_equal,
        "period_days": period_days,
        "approx_period": approx_period,
        "transit_depth": transit_depth,
        "planet_radius_km": planet_radius_km,
        "planet_radius_earths": planet_radius_earths,
        "planet_tag": planet_tag,
        "tag": planet_tag,
        "planet_class": planet_tag,
        "classification": planet_tag,
        "orbital_distance_au": orbital_distance_au,
        "orbital_distance_km": orbital_distance_km,
        "habitable_zone_au": habitable_zone_au,
        "distance_from_hz_au": distance_from_hz_au,
    }


# ==============================================================================
# 4. EXECUTION AND REPORT PRESENTATION
# ==============================================================================
def main():
    print("=" * 80)
    print("STAC WARS - PS 3: EXOPLANET HUNTERS (OPERATION DIM STAR)")
    print("Official Analysis Report & Computational Solution")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("EXPLICIT ASSUMPTIONS")
    print("=" * 80)
    print("1. Maximum recorded relative brightness (1.0000) corresponds to normal flux (Fnormal).")
    print("2. Dips in brightness represent transits of an opaque orbiting body across stellar disk.")
    print("3. PERIOD CRITERION: A definitive orbital period is accepted ONLY if ALL consecutive")
    print("   transit intervals are strictly identical (delta_t_1 = delta_t_2 = ...). If consecutive")
    print("   gaps differ, a single Keplerian period cannot be unambiguously determined.")
    print("4. Transit depth equation: delta = (Rp / Rs)^2 => Rp = Rs * sqrt(delta).")
    print("   (The PDF equation box printed delta ≈ (Rs/Rp)^2, which is an inverted typo).")
    print("5. Orbital distance obeys the simplified Kepler's Third Law: P^2 = a^3 / M.")
    print("6. Habitable zone center is calculated via dHZ = sqrt(L / L_sun) AU.")

    results = {name: analyse_system(name) for name in STELLAR_PROPERTIES}

    # --------------------------------------------------------------------------
    # PART A: DETECT THE EXOPLANETS (4 MARKS)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART A: DETECT THE EXOPLANETS (4 MARKS)")
    print("=" * 80)
    print("Questions 1-4 Analysis for STAC-1, STAC-2, and STAC-3:")

    for name, res in results.items():
        print(f"\n[{name}]")
        # Q1: Transit detection
        print(f"  1. Transit Detection:")
        print(f"     - Transit dip events observed at time (days): {res['transit_days']}")
        print(f"     - Consecutive gaps between dips: {res['intervals']} days")
        print(f"     - Finding: Repeated brightness dips are detected, indicating candidate exoplanet transits.")

        # Q2: Orbital Period
        print(f"  2. Orbital Period Determination:")
        if res["all_intervals_equal"]:
            print(f"     - Gaps: All {len(res['intervals'])} consecutive gaps are equal to {res['period_days']:.1f} days.")
            print(f"     - RESULT: Periodic transit CONFIRMED. Orbital Period P = {res['period_days']:.1f} days.")
        else:
            print(f"     - Gaps: Consecutive intervals {res['intervals']} are NOT all equal.")
            print(f"     - RESULT: Period CANNOT be determined under the strict uniformity criterion.")
            print(f"       (Note: If approximate mode interval is considered, P ≈ {res['approx_period']:.1f} days).")

        # Q3: Transit depth
        depth = res["transit_depth"]
        f_norm = res["normal_brightness"]
        f_trans = res["minimum_brightness"]
        print(f"  3. Transit Depth (delta):")
        print(f"     - delta = (Fnormal - Ftransit) / Fnormal = ({f_norm:.4f} - {f_trans:.4f}) / {f_norm:.4f}")
        print(f"     - delta = {depth:.6f} ({depth * 100:.3f}%)")

    # Q4: Explanation
    print("\n  4. Physical Explanation:")
    print("     A periodic decrease in stellar brightness occurs when an exoplanet passes directly")
    print("     between the host star and the observer (along our line of sight). During transit,")
    print("     the opaque planetary disk blocks a fraction of the star's emitted light proportional")
    print("     to the area ratio (Rp / Rs)^2, creating a temporary, recurring dip whose regular")
    print("     interval reflects the orbital period dictated by Kepler's laws.")

    # --------------------------------------------------------------------------
    # PART B: DETERMINE THE PLANET SIZE (4 MARKS)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART B: DETERMINE THE PLANET SIZE (4 MARKS)")
    print("=" * 80)
    print("Questions 5-7 Planetary Radius and Classification:")

    for name, res in results.items():
        star = res["star_properties"]
        rs_km = star["radius"] * SOLAR_RADIUS_KM
        rp_km = res["planet_radius_km"]
        rp_earth = res["planet_radius_earths"]
        p_tag = res["planet_tag"]
        delta = res["transit_depth"]

        print(f"\n[{name} Candidate - Tag: {p_tag}]")
        print(f"  Host Star Radius (Rs) = {star['radius']:.2f} R_sun = {rs_km:,.0f} km")
        print(f"  5. Radius in kilometres:")
        print(f"     Rp = Rs * sqrt(delta) = {rs_km:,.0f} * sqrt({delta:.6f})")
        print(f"     Rp = {rp_km:,.1f} km")
        print(f"  6. Radius in terms of Earth's radius (R_Earth = {EARTH_RADIUS_KM:,.0f} km):")
        print(f"     Rp / R_Earth = {rp_km:.1f} / {EARTH_RADIUS_KM:.0f} = {rp_earth:.2f} R_Earth")
        print(f"  7. Classification / Tag: [{p_tag}]")

    print("\n" + "-" * 80)
    print("QUESTION 7: PLANETARY SIZE TAGGING & CLASSIFICATION SUMMARY")
    print("-" * 80)
    print("Classification Categories (Specified in PS 3 Question 7):")
    print("  • Earth-sized   : Rp <= 1.25 Earth radii")
    print("  • Super-Earth   : 1.25 < Rp <= 2.0 Earth radii")
    print("  • Neptune-sized : 2.0 < Rp <= 6.0 Earth radii")
    print("  • Jupiter-sized : Rp > 6.0 Earth radii")
    print("\nTagged Exoplanets:")
    for name, res in results.items():
        print(f"  • {name} planet: Radius = {res['planet_radius_earths']:.2f} R_Earth ({res['planet_radius_km']:,.0f} km) -> TAGGED AS: [{res['planet_tag']}]")

    # --------------------------------------------------------------------------
    # PART C: DETERMINE THE PLANETARY ORBITS (4 MARKS)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART C: DETERMINE THE PLANETARY ORBITS (4 MARKS)")
    print("=" * 80)
    print("Questions 8-10 Orbital Distance using Kepler's Third Law (P^2 = a^3 / M):")

    for name, res in results.items():
        print(f"\n[{name} Planet - Tag: {res['planet_tag']}]")
        if res["orbital_distance_au"] is not None:
            p_days = res["period_days"]
            p_yrs = p_days / DAYS_PER_YEAR
            m = res["star_properties"]["mass"]
            a_au = res["orbital_distance_au"]
            a_km = res["orbital_distance_km"]

            print(f"  Period P = {p_days:.1f} days = {p_yrs:.4f} years | Stellar Mass M = {m:.2f} M_sun")
            print(f"  8. Orbital distance in AU:")
            print(f"     a = (P^2 * M)^(1/3) = ({p_yrs:.4f}^2 * {m:.2f})^(1/3) = {a_au:.4f} AU")
            print(f"  9. Distance in kilometres (1 AU = {AU_KM:,.0f} km):")
            print(f"     Distance = {a_au:.4f} * {AU_KM:,.0f} = {a_km:,.0f} km ({a_km / 1e6:.2f} million km)")
            print(f"  10. Comparison with Earth's distance from the Sun (1.0 AU):")
            print(f"      Orbital distance is {a_au:.3f} times Earth's distance from the Sun ({a_au * 100:.1f}% of 1 AU).")
        else:
            print("  8. Orbital distance (AU): NOT DETERMINED")
            print(f"     Reason: Transit intervals {res['intervals']} are not strictly uniform.")
            print("  9. Distance (km): N/A")
            print("  10. Comparison with Earth: N/A")
            if res["approx_period"] is not None:
                p_approx_yrs = res["approx_period"] / DAYS_PER_YEAR
                m = res["star_properties"]["mass"]
                a_approx_au = (p_approx_yrs**2 * m) ** (1.0 / 3.0)
                a_approx_km = a_approx_au * AU_KM
                print(f"     [Sensitivity Note: If approximate P ≈ {res['approx_period']:.0f} d was used,")
                print(f"      a ≈ {a_approx_au:.4f} AU ({a_approx_km:,.0f} km), {a_approx_au:.3f}x Earth distance]")

    # --------------------------------------------------------------------------
    # PART D: FIND THE MOST PROMISING WORLD (3 MARKS)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART D: FIND THE MOST PROMISING WORLD (3 MARKS)")
    print("=" * 80)
    print("Questions 11-13 Habitability Evaluation & Candidate Selection:")

    # Habitable Zone Summary
    print("\nHabitable Zone Comparison (dHZ = sqrt(L / L_sun) AU):")
    for name, res in results.items():
        l = res["star_properties"]["luminosity"]
        dhz = res["habitable_zone_au"]
        a_str = f"{res['orbital_distance_au']:.4f} AU" if res["orbital_distance_au"] else "Undetermined"
        print(f"  - {name} [{res['planet_tag']}]: L = {l:.2f} L_sun => Habitable Zone Center dHZ = {dhz:.4f} AU (Planet a = {a_str})")

    # Filter detected candidates with valid orbital parameters
    confirmed_candidates = {
        name: res for name, res in results.items() if res["orbital_distance_au"] is not None
    }

    best_candidate_name = min(
        confirmed_candidates,
        key=lambda n: confirmed_candidates[n]["distance_from_hz_au"]
    )
    best = confirmed_candidates[best_candidate_name]

    print(f"\n11. Most Promising Candidate for Habitability Studies:")
    print(f"    >>> {best_candidate_name} [Tag: {best['planet_tag']}] <<<")

    print("\n12. Evidence Supporting This Choice (At least 3 pieces of evidence):")
    print(f"    Evidence 1: Strictly Regular & Confirmed Periodic Orbit")
    print(f"      {best_candidate_name} is the ONLY stellar system where consecutive transit gaps are")
    print(f"      completely uniform ([80, 80] days), definitively proving a stable, repeatable Keplerian orbit")
    print(f"      with period P = {best['period_days']:.0f} days.")
    print(f"    Evidence 2: Favourable Planetary Size & Atmospheric Retention")
    print(f"      The planet has a radius of {best['planet_radius_earths']:.2f} R_Earth ({best['planet_radius_km']:,.0f} km),")
    print(f"      classifying and tagging it as a [{best['planet_tag']}]. This provides sufficient surface gravity")
    print(f"      to retain a substantial, protective atmosphere and potentially host volatile/oceanic layers.")
    print(f"    Evidence 3: Proximity to Temperate Zone of a Stable K-dwarf")
    print(f"      {best_candidate_name} is an orange K-dwarf (T = 5000 K, L = 0.40 L_sun). K-type stars provide")
    print(f"      exceedingly stable main-sequence lifetimes (15-30 billion years) without the deadly UV flare")
    print(f"      activity characteristic of M-dwarfs (STAC-3). Its orbit (0.337 AU) places it comfortably")
    print(f"      within the warm inner realm of its habitable zone (dHZ = {best['habitable_zone_au']:.3f} AU).")

    print("\n13. Suggested Additional Astronomical Observation / Measurement:")
    print("    Transmission Spectroscopy (e.g., using the James Webb Space Telescope - JWST):")
    print("    During transit, stellar photons filter through the planet's atmospheric annulus.")
    print("    Measuring wavelength-dependent transit depths reveals atomic and molecular absorption")
    print("    signatures (such as H2O, CO2, CH4, and atmospheric biosignatures like O3 or DMS),")
    print("    verifying atmospheric composition, temperature profile, and habitability potential.")
    print("    (Complementary: Radial Velocity measurements to constrain mass and bulk density).")

    # --------------------------------------------------------------------------
    # SUBMISSION REQUIREMENTS CHECKLIST (QUESTIONS 14-18)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("SUBMISSION CHECKLIST (QUESTIONS 14-18)")
    print("=" * 80)
    print("14. Detection and identification of possible exoplanets:")
    print("    -> Completed in Part A (Dips identified for all 3 stars; strictly periodic orbit confirmed for STAC-2).")
    print("15. Calculations of planetary radii & size tagging:")
    for name, res in results.items():
        print(f"    -> {name} planet: Radius = {res['planet_radius_earths']:.2f} R_Earth ({res['planet_radius_km']:,.0f} km) => Tag: [{res['planet_tag']}]")
    print("16. Calculations of orbital distances:")
    print(f"    -> Completed in Part C: STAC-2 orbital distance = {results['STAC-2']['orbital_distance_au']:.3f} AU "
          f"({results['STAC-2']['orbital_distance_km']:,.0f} km).")
    print("17. Comparison of detected planets and identification of most promising candidate:")
    print(f"    -> Completed in Part D: {best_candidate_name} [{best['planet_tag']}] identified as the prime candidate with detailed multi-point evidence.")
    print("18. Clear reasoning, formulas, and stated assumptions:")
    print("    -> Fully documented and printed in the sections above.")
    print("=" * 80)
    print("MAY THE CODE BE WITH YOU!")
    print("=" * 80)


if __name__ == "__main__":
    main()
