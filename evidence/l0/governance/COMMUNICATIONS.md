# Host Communications Record: `sandia-battery-degradation-s1`

## 1. Bulk Data Acquisition & Observation Horizon Inquiry

* **Status:** `TRANSMITTED / AWAITING_HOST_RESPONSE`
* **Recipient:** `info@batteryarchive.org`
* **Sender:** Ivan Nestorov (VolMax Studio Lab)
* **Date:** 2026-09-05T20:33:00Z
* **Subject:** SNL degradation dataset — bulk access and 2020 study observation horizon

### Exact Transmitted Text:
```text
Dear BatteryArchive team,

I am conducting a preregistered independent computational reconstruction of the Sandia National Laboratories degradation study published by Preger et al., Journal of The Electrochemical Society 167, 120532 (2020), DOI: 10.1149/1945-7111/abae37.

Our public BatteryArchive metadata snapshot identifies 86 SNL cells associated with this study. Before acquiring the cycling files, I would like to confirm the supported acquisition route and one point that is important for reproducing the publication-era results correctly.

1. Bulk acquisition: What is the supported method for obtaining the cycle-summary and/or time-series files for the complete SNL degradation-study cohort? The BatteryArchive FAQ directs multi-cell downloads to this address, so we do not want to bypass the intended bulk-access process.

2. Reuse / redistribution: Do any additional reuse conditions apply to this SNL degradation dataset beyond the BatteryArchive citation/code-of-conduct guidance? We do not intend to redistribute the raw cycling files; our public repository would contain only acquisition metadata, hashes, code and derived audit outputs unless you explicitly permit otherwise.

3. Publication-era observation horizon: What was the data cutoff, study-end date, or per-cell observation horizon used for Figure 2a in Preger et al. (2020)? BatteryArchive notes that cycling continued beyond the publication-era study. For a historical reconstruction we need to censor the present-day records to the same horizon used to generate Figure 2a, rather than allowing later measurements to change the measured-versus-extrapolated classification.

If there was no single calendar cutoff, a description of how the Figure 2a dataset vintage was defined (for example, per-cell final observations or a frozen archive snapshot) would be equally useful.

4. Method clarification, if available: Is there a documented implementation detail for the Figure 2a EFC-to-80%-capacity calculation, specifically:
* which capacity-check value served as the initial capacity reference;
* whether the 80% endpoint was the first observed discrete crossing or an interpolated crossing; and
* whether “total capacity throughput / nominal capacity” was implemented from discharge capacity only or by another convention?

These questions are being resolved before any verdict-bearing data analysis so that the estimator and observation horizon can be frozen in advance.

Thank you for your help.

Best regards,
Ivan Nestorov
VolMax Studio Lab
```

### Response Tracking:
* **Incoming Response File:** `evidence/l0/source_pages/batteryarchive_host_response.eml` (to be saved verbatim with full cryptographic headers upon receipt).
* **Dependencies Dependent on Response:**
  - `G-L0-5A`: Authorized bulk download method.
  - `G-L0-5B`: Redistribution terms.
  - `OBSERVATION_HORIZON`: Resolution of `HALT_OBSERVATION_HORIZON_UNDETERMINED`.
  - `ESTIMATOR_SPECIFICATION`: Formal pinning of $Q_0$, EFC throughput formulation, and $N_{80}$ crossing rule.
