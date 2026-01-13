# Compliance Questions Dataset

This document provides a set of 15+ sample questions designed to challenge the RAG system and verify its grounding and retrieval accuracy across all ingested data files.

## 1. Full Material Disclosure (FMD) Challenges
*Target File: `FMD_Test_Corporation.pdf`*

| # | Question | Expected Outcome |
|---|---|---|
| 1 | "How much Lead (Pb) is in part TCC-8334-A?" | **55.24%**. The part should be flagged as "Not Compliant". |
| 2 | "Is part TC-3541-A compliant according to the FMD report?" | **Yes**. It contains Silver and Aluminum and is marked as "Compliant". |
| 3 | "Which part contains Polyamide 6/6 (PA66) at exactly 56.79% weight?" | **TCX-6419-C** (Rev R2). |
| 4 | "What is the CAS No. for Silicon Dioxide in part TC-2410-F?" | **7631-86-9**. |
| 5 | "List all parts that contain Gold (Au) according to the FMD report." | **TP-1198-B, TC-9053-E, TCX-2705-D, TCC-8334-A, TCC-1622-C, TR-5783-B**. |

## 2. REACH Certificate Challenges
*Target File: `REACH_Certificate_of_Compliance_Test_Corporation.pdf`*

| # | Question | Expected Outcome |
|---|---|---|
| 6 | "Is part PN=TCC-9856-B listed in the REACH Certificate?" | **Yes**. It appears multiple times (e.g., Tier 2 and Tier 3). |
| 7 | "Who is the authorized signatory for the REACH document?" | **Avery Morgan**, Compliance & Product Stewardship Manager. |
| 8 | "What internal procedure covers Restricted Substances Management?" | **TC-QSP-17**. |
| 9 | "What is the article-level threshold for SVHC content assessment?" | **0.1% w/w**. |
| 10 | "What regulation number is referenced for REACH compliance?" | **Regulation (EC) No 1907/2006**. |

## 3. Part Measurement Challenges
*Target File: `part_measurements_test_corporation.html`*

| # | Question | Expected Outcome |
|---|---|---|
| 11 | "What is the measured average for the Pin Pitch of TC-3541-A?" | **2.55 mm**. |
| 12 | "Did part TR-7820-D pass the Connector Height (H) measurement?" | **Fail**. The measured average was 8.63 mm against a nominal of 8.50 ±0.10. |
| 13 | "What method was used to measure the Board Thickness of TP-1198-B?" | **Micrometer**. |
| 14 | "What is the recorded Max value for the Overall Length of TC-3541-A?" | **25.04 mm**. |

## 4. System Robustness & Grounding
*Targeting Grounding Threshold and Cross-File Knowledge*

| # | Question | Expected Outcome |
|---|---|---|
| 15 | "What is the revision number (Rev) for part TC-3541-A in the reports?" | **Rev R3**. (Verified across both PDF and HTML reports). |
| 16 | "What is the weight limit for a package sent to Pluto?" | **Information not found**. Should trigger the "Safe Failure" (similarity < 0.6). |
| 17 | "Does Test Corporation use 23°C for its measurement environment?" | **Yes**. Note says: 23°C ±2°C; RH 40–60%. |

---
**Note:** These questions verify that the system is correctly parsing tables (Markdown conversion), respecting strict grounding, and correctly attributing sources (PDF vs HTML).
