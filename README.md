# NDHS-microdata-python-code
This Python code transforms National Survey Microdata into clean, analysis-ready datasets. Processes raw microdata from large-scale national surveys. Originally developed and tested using microdata from the 2018 NDHS microdata.  Output Generates a structured readable dataset suitable for various statistical projects.
# DHS 2018 Nigeria Microdata (Cleaned & Processed)

## Overview 📖

This repository contains a cleaned and structured version of the **2018 Nigeria Demographic and Health Survey (NDHS)** microdata, transformed into **CSV format** for ease of analysis. The dataset has been processed to focus on **child survival analysis** using time-to-event (survival) methods. It includes properly formatted variables, event indicators, and time variables consistent with survival analysis standards.


## File Contents 📂

* **raw_data/** → Extracted original DHS raw files (.DAT/.SAV).
* **cleaned_data/** → Final CSV files, ready for analysis.
* **code/** → Scripts for cleaning, transformation, and exploratory checks (Python).
* **docs/** → Metadata, dictionary, usage, methodology notes and many others.
* **summary/** → Descriptive statistics and aggregated tables.

---

## Methods Note 🛠️

The raw DHS birth recode files (BR) were transformed into a cleaned CSV using the following steps:

1. **Data Import & Selection** → Selected relevant variables (child’s survival status, age at death, survey date, etc.).
2. **Event Definition** →

   * `event = 1` → Child died before the survey.
   * `event = 0` → Child alive at the time of the survey.
3. **Time Variable Construction** →

   * If `event = 1` → `time = age at death in months (b7)`.
   * If `event = 0` → `time = age at survey in months (b19)`.
   * If death occurred before 1 month → coded as `time = 0`.
4. **Censoring & Cleaning** → Alive cases are right-censored; implausible values removed.
5. **Export** → Final dataset written to CSV with metadata dictionary.

---

## Variable Dictionary 📑

| Variable      | DHS Code | Description                                 |
| ------------- | -------- | ------------------------------------------- |
| `id`          | CaseID   | Unique household/respondent ID              |
| `event`       | Derived  | 1 = child died, 0 = child alive             |
| `time`        | Derived  | Survival/censoring time (months)            |
| `b7`          | b7       | Age at death in months (if dead)            |
| `b19`         | b19      | Age of child in months at survey (if alive) |
| `sex`         | b4       | Sex of child (1 = male, 2 = female)         |
| `birth_order` | bord     | Birth order of child                        |
| `mother_age`  | v012     | Mother’s age at time of survey              |
| `residence`   | v025     | Place of residence (urban/rural)            |
| `region`      | v024     | Geopolitical zone of residence              |

*Note: Only relevant variables for survival analysis are retained; others available on request.*

---

## Summary Statistics 📊

* **Total children:** 33,924 
* **Deaths observed:** 3,211
* **Alive (censored):** 30,713
* **Span survival time:** 0 month to 59 months

---

## Subject/Abstract 📌

This dataset is a cleaned and restructured version of the **2018 Nigeria Demographic and Health Survey (NDHS)** microdata, optimized for **child mortality survival analysis**. The dataset provides well-labeled, analysis-ready CSV files with consistent event and time variables for epidemiological and demographic research.

---

## Tags/Keywords 🏷️

`Nigeria DHS` · `NDHS 2018` · `child mortality` · `survival analysis` · `time-to-event data` · `censoring` · `public health` · `demographic survey` · `microdata` · `data analysis`

---

## Citation 📚

If you use this dataset, please cite:

> National Population Commission (NPC) [Nigeria] and ICF. 2019. *Nigeria Demographic and Health Survey 2018*. Abuja, Nigeria, and Rockville, Maryland, USA: NPC and ICF.

---

## License ⚖️

This dataset is based on publicly available DHS microdata. Redistribution follows **DHS Program data usage policy**. Please consult the [DHS Program website](https://dhsprogram.com) for details.

---

## Contact ✉️

For questions, collaborations, or clarifications:

**Maintainer:** Uthman Adesola (SUNEXUS)
**Email:** uthmanrsm@gmail.com
**GitHub:** [github.com/SirUTHYsir](https://github.com/SirUTHYsir)
