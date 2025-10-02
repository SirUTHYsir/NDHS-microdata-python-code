# HOW TO USE

Below is an explicit, clear, and detailed description of the time and event variables, how they were derived from DHS variables, what their values mean, special cases, and recommended checks.

## Time & Event detailed explanation 

* `Time:`  Follow-up duration (months)
* `Definition:` Time is the child’s exposure time measured in months. It represents the time from birth until the event (death) or until censoring (the date of interview, for children who are alive).

## Derivation (DHS source variables):
* **`b7—`** Age at death (months) (DHS): used if the child died.
* **`b19—`** Child’s age in months at interview/survey: used if the child is alive.

## Rule used to compute time:

* if `event == 1`:     `time = b7`      # child died → `time` = `age at death in months`
* else `(event == 0)`:  `time = b19`    # child alive  → `time` = `age at survey (censoring time) in months`
*Units: months (numeric, can be integer or float).

## Special coding:
* `time = 0` → death at birth (neonatal death within 1 month). This is a valid value meaning the child died at/very soon after birth.
* For all living children `(event = 0)`, time must be ≥ 0 and should reflect their current age at interview.

## Why we do this:

Survival analysis requires a non-ambiguous follow-up time for every record:
For those who died, the time until the event is age at death.
For those still alive, we record the length of observation (censoring time) — their age at interview — so they contribute correct exposure time to the risk set.

## Practical notes & pitfalls to check for if reusing the python file.
Ensure `b19` is present in the KR file, `b19` usually exists and is the recommended censoring time. If `b19` is missing, compute age at survey as `v008` - `b3` (CMC difference) only if v008 and b3 are available and correctly coded.
Check for negative or implausible times (e.g., time < 0 or time > 59): investigate and correct or drop problematic records.
Decide whether to cap follow-up at 59 months for under-5 analyses (under-5 = < 60 months). If you cap, use time = min(time, 59). Document this choice.
Keep time numeric (float or int). Round only for display if you want decimals; modeling functions accept numeric months.


## Examples:

| `b5` (alive) |	`b7` (age at death) |	`b19` (age at survey)	| Event  |	Time	|        Meaning            |
|  ----------  |  ------------------  |  -------------------  |  ----  |  ----  |  -----------------------  |
| 0 (dead)	   |     0                |      	—	              |   1    | 	0	    |  Died at birth (neonatal) |
| 0 (dead)	   |     10               |       —    	          |   1    |	10	  |  Died at 10 months        |
| 1 (alive)	   |     NaN	            |       24	            |   0	   |  24	  | Alive; censored at 24mths |
________________________________________

## Event: Event Indicator (Death Vs Censored)

**Definition:** →
* Binary indicator for the occurrence of the event (death) during follow-up.

**Coding used here (analysis-friendly):** →
* `event = 1` → child died (event occurred)
* `event = 0` → child alive at interview (censored)

**Derivation (DHS source variable):** →

* `b5:` DHS survival status: `1 = alive`, `0 = dead`.

We recode DHS b5 to the analysis event as follows:
* `event = 1` if `b5 == 0` else `0`
(i.e., reverse DHS coding so event = 1 means death.)

## WHY RECODE THIS WAY?

Most survival analysis libraries and textbooks expect `event = 1` for the event of interest (death) and `event = 0` for censoring. This standardization avoids confusion in KM and Cox functions.

## Practical notes & pitfalls to check:
Verify there are no other codes in b5 (e.g., missing codes). Handle missing as NaN or drop depending on your protocol.
Confirm consistency between event and time:
**If `event == 1`, time should be derived from `b7` and not from `b19`.
**If `event == 0`, time should be derived from `b19`.
**If `event == 1`, but `b7` is missing → investigate and decide whether to drop or impute.
Confirm event dtype is integer (0/1) when feeding into models.


## VARIABLES DICTIONARY
This dictionary explains the variables included in the cleaned child mortality dataset (child_mortality.csv).

**Each entry shows:
* Variable Name (in cleaned dataset)
* Description
* Source DHS Variable(s)
* Notes / Recoding

## CORE VARIABLES

|   Variable    |                	Description	                                   |   DHS   |             Notes/Recording                                                                                                                                |
|  -----------  |  ------------------------------------------------------------  |  -----  |  --------------------------------------------------------------------------------------------------------------------------------------------------------  |
|  household_id |	Household identifier (unique per household in the survey)	     | hhid    |	Combines cluster + household number.                                                                                                                      |
|  region       |	Region / state groupings (coded numerically e.g. 1,2,3…)	     | v024    |	DHS region variable (Nigeria has 6 geopolitical zones / 37 states depending on dataset).                                                                  |
|    area	      | Place of residence (urban/rural)	                             | v025    |  Recoded: 1 = Urban, 2 = Rural.                                                                                                                            |
|    wealth     |	Household wealth index quintile                                | v190    |	DHS wealth index: 1 = Poorest … 5 = Richest.                                                                                                              |
|   Education   |	Mother’s highest education level	                             | v106    |	Recoded: 0 = No education, 1 = Primary, 2 = Secondary, 3 = Higher.                                                                                        |
|   mother_age  |	Age of mother at time of child’s birth	                       | v012,b3 | Computed: mother’s age at survey minus child’s age in months.                                                                                              |
|      time     |	Child’s age at death in months (if dead)	                     |   b7    |	If event=1, holds months lived. If event=0 (alive), coded as NaN/blank.                                                                                   |
|     event     |	Child mortality outcome	                                       |   b5    |	Recoded: 1 = Child died, 0 = Alive at survey. (Note: DHS b5 is originally 1=Alive, 0=Dead; reversed here for survival analysis consistency).              |

## Derived / Analytical Variables

|   Variable    |                	Description	                                   |   DHS Source   |             Notes/Recording                      |
|  -----------  |  ------------------------------------------------------------  |  ------------  |  ----------------------------------------------  |
|   Neonatal    |               Neonatal death indicator                         |       b7       |    1 = died before 1 month, 0 = otherwise.       |
|    infant     |                  	Infant death indicator                       |       b7	      |    1 = died before 12 months, 0 = otherwise.     |
|    under5	    |               Under-five death indicator	                     |       b7	      |    1 = died before 60 months, 0 = otherwise.     |

** `Time` = Follow-up time in months. For children who died (event = 1), time = b7 (age at death in months). For children who were alive at interview (event = 0), time = b19 (age of child in months at survey). time = 0 indicates death at birth (neonatal). Units = months.

** `Event` = Event indicator (binary). 1 = child died (DHS b5 == 0), 0 = child alive / censored (DHS b5 == 1).
