# Evidentiary Finding: Access-Layer Drift & Acquisition Interface Persistence

**Finding ID:** `FINDING-L0-ACCESS-DRIFT-001`  
**Date:** 2026-09-05  
**Instance:** `sandia-battery-degradation-s1`  
**Evaluated Study:** Preger et al., *J. Electrochem. Soc.* 167, 120532 (2020), DOI: [10.1149/1945-7111/abae37](https://doi.org/10.1149/1945-7111/abae37)  
**Evaluated Claim:** *"All cycling files have been made publicly available at batteryarchive.org, a recently developed repository for visualization and comparison of battery data, to facilitate future experimental and modeling efforts."* (Preger et al. 2020, Abstract, p. 120532-1)

---

## 1. Executive Summary

During telemetry acquisition execution for the independent computational reconstruction of Preger et al. (2020), direct automated retrieval of the 86 Sandia National Laboratories (SNL) cell cycle summaries via the historically documented public download pattern failed with consistent `HTTP 404 Not Found` responses across all cell files.

Independent investigation confirms that:
1. The historical 2021 public data transfer protocol (`https://www.batteryarchive.org/data/[cell_id]_cycle_data.csv`) is no longer exposed as a static web endpoint on the contemporary host infrastructure.
2. The current host governance policy mandates host-mediated dataset access for multi-cell bulk downloads (BatteryArchive FAQ: *"Please contact info@batteryarchive.org for information on how to download datasets"*).
3. Third-party data science frameworks (e.g. Microsoft BatteryML) independently document that Sandia (SNL), UL-PUR, and HNEI public datasets on BatteryArchive no longer provide direct unauthenticated download links and require manual host authorization.
4. Sandia National Laboratories maintains an authentic archived GitHub repository ([`sandialabs/battery-archive-sandbox`](https://github.com/sandialabs/battery-archive-sandbox/tree/main/data/snl)) containing historical raw NMC cycling archives (`SNL_18650_G5_NMC1.zip` ~90.8 MB, `SNL_18650_G5_NMC2.zip` ~86.9 MB), providing an independent physical provenance reference for a subset of the cohort.

**Controlled P10 Audit Finding:**
> *The publication-era public-data claim is not presently reproducible through the historical direct-download interface; current bulk acquisition requires host-mediated access.*

This finding does not indicate that data was unavailable in 2020–2021, but establishes a concrete instance of **access-layer drift** affecting computational auditability over multi-year horizons.

---

## 2. Historical Acquisition Architecture (2021 Baseline)

As preserved in the project evidence base ([`evidence/l0/source_pages/batteryarchive_data_transfer.py`](../source_pages/batteryarchive_data_transfer.py)), the original public Python data transfer utility authored by Valerio De Angelis (2021) implemented direct HTTP GET downloads using the canonical pattern:

```python
# batteryarchive_data_transfer.py (De Angelis 2021, Lines 130-150)
prefix = "https://www.batteryarchive.org/data/"
file_name = cell_id.replace("/", "-")
cycle_data_url = prefix + file_name + "_cycle_data.csv"
timeseries_data_url = prefix + file_name + "_timeseries.csv"
```

Under this interface, any researcher could deterministically fetch raw cycler summary and time-series streams by cell identifier without authentication or manual ticketing.

---

## 3. Present Direct Acquisition Failure (2026 Audit Run)

During telemetry acquisition execution for `run-002-a1h`, an automated retrieval pass was conducted across all 86 expected SNL cohort cells. Every request returned an unhandled HTTP 404 from the host web server:

```http
HTTP/1.1 404 Not Found
Server: nginx/1.22.0 (Ubuntu)
Date: Sat, 05 Sep 2026 21:46:28 GMT
Content-Type: text/html
Content-Length: 162
Connection: keep-alive
```

Full acquisition logs capturing all 86 failed endpoints are preserved in:
- [`runs/run-002-a1h/acquisition_stdout.log`](../../../runs/run-002-a1h/acquisition_stdout.log)
- [`runs/run-002-a1h/acquisition_stderr.log`](../../../runs/run-002-a1h/acquisition_stderr.log)

---

## 4. Current Host Governance & Independent Confirmation

### 4.1 Host FAQ Requirement
BatteryArchive's official FAQ ([`evidence/l0/source_pages/batteryarchive_faq.html`](../source_pages/batteryarchive_faq.html#L98-L102)) explicitly confirms the transition to host-mediated bulk delivery:
> **Q: How do I download data for many cells at once?**  
> **A:** *Please contact info@batteryarchive.org for information on how to download datasets.*

### 4.2 Third-Party Framework Confirmation (BatteryML)
Microsoft's open-source BatteryML framework documents the same interface constraint: SNL, UL-PUR, and HNEI dataset download URLs are no longer statically resolvable on BatteryArchive, requiring external users to request direct file transfers from dataset maintainers.

### 4.3 Dispatched Host Inquiry
On 2026-09-05, a formal inquiry was dispatched to `info@batteryarchive.org` requesting:
1. The supported bulk retrieval mechanism for the 86 SNL degradation cell files.
2. Confirmation of the historical laboratory observation horizon / cutoff timestamp for the 2020 study.

Tracking record: [`evidence/l0/governance/COMMUNICATIONS.md`](../governance/COMMUNICATIONS.md).

---

## 5. Secondary Historical Artifact: Sandia Labs GitHub Archive

Sandia National Laboratories maintains a public archived repository:
- **Repository:** [`https://github.com/sandialabs/battery-archive-sandbox`](https://github.com/sandialabs/battery-archive-sandbox)
- **Path:** `data/snl/`
- **Artifacts:**
  - `SNL_18650_G5_NMC1.zip` (~90.8 MB)
  - `SNL_18650_G5_NMC2.zip` (~86.9 MB)

These archives contain raw historical cycling CSV files for NMC cells from the study. While this represents an authentic publisher-hosted artifact, it covers only a partial subset of the 86-cell cohort (omitting LFP and NCA cells in standardized BatteryArchive schema). Consequently, it is logged here as an **independent provenance cross-check** rather than substituted into `run-002-a1h`.

---

## 6. Scientific & Battery Passport Implications

This finding illustrates a critical dimension of long-term computational auditability:

1. **Provenance vs. Accessibility:** A scientific claim or Digital Battery Passport may possess perfect cryptographic hashing, DOI metadata, and rigorous method descriptions; however, if the underlying raw data acquisition interface suffers bit rot or policy changes over a 5-to-10 year lifecycle, third-party independent verifiability becomes degraded.
2. **Access-Layer Governance:** Autonomous auditing systems and regulatory verifiers must treat acquisition routes, interface contracts, and data-host SLAs as explicit audit variables, rather than assuming unvarying static URL persistence.
3. **Execution State Transition:** In accordance with P10 governance invariants, `run-002-a1h` is placed in state:
   $$\text{State} = \text{WAITING\_FOR\_SUPPORTED\_ACQUISITION\_ROUTE}$$
   Target A1-H evaluation remains frozen and unblocked, awaiting physical byte ingestion via the confirmed host-mediated route.
