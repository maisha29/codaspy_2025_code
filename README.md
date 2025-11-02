# codaspy_2025_code
HMAM (Harmonic Mean–Arithmetic Mean) Ratio and RUC Calculation

This repository implements a complete data processing and evaluation pipeline for detecting cyberattacks using the Residual Under Curve (RUC) metric. The scripts prepare, transform, and evaluate time-series data collected from networked control systems or communication buses (e.g., CAN, DNP3, or SOME/IP).

📂 Repository Structure
├── id_segregation.py
├── setup_ruc_data.py
├── ratio_calculation.py
├── ruc_cv_fa_md.py
├── on_off_testset.py
├── on_off_perform_ev.py
└── README.md

🧩 Script Descriptions
1. id_segregation.py

Parses raw network log files (e.g., Impersonation_attack_dataset.csv) and extracts timestamp, CAN ID, RTR flag, and payload.
It identifies transitions between RTR=100 and RTR=000 for each unique ID, measures the offset between them, and exports the results to imp_offset_results.csv.

Output:
imp_offset_results.csv — contains ID, Imp Offset, and Dataframe Payload.

2. setup_ruc_data.py

Computes the Residual Under Curve (RUC) metric for all datasets matching Test_imp_155*.csv.
For each frame length and kappa value, it:

Calculates safe margins (mean ± kappa × σ)

Derives stateless residuals

Accumulates residuals over a rolling frame (F)

Output:
RUC result files named like RUC_test_imp_f{frame_length}_k{kappa}_155.csv.

3. ratio_calculation.py

Groups benign baseline data (Attack_free_all_IDs.csv) into windows of size 155.
For each window, it calculates:

Arithmetic mean and harmonic mean of time_interval

Ratio = (harmonic mean) / (arithmetic mean)

This produces a per-window statistical profile used later for attack detection.

Output:
AF_all_ID_grouped155.csv — containing window number, ratio, and timestamp.

4. ruc_cv_fa_md.py

Performs false alarm (FA) and miss detection (MD) evaluation on labeled datasets.
It reads both the ratio dataset and RUC validation file, splits benign and attack portions, and computes:

False alarm rate (benign values < threshold)

Miss detection rate (attack values ≥ threshold)

Time to detection between the first attack window and detection event.

Output:
Console logs of FA, MD, and detection latency.

5. on_off_testset.py

Generates alternating ON–OFF attack test sets from labeled data (Test_Imp_200.csv).
It repeats benign and attack sequences in a controlled pattern (e.g., 70 on/off samples per cycle).

Output:
Files like Imp_new_test_200_on_off_70.csv.

6. on_off_perform_ev.py

Evaluates model performance on multiple ON–OFF test sets.
It finds matching ratio and validation files, applies the same detection threshold, and computes:

False alarm rate

Miss detection rate

Time to detection per test file.

Output:
Console summary of FA, MD, and detection delay for each test case.

🧠 Workflow Overview

Preprocess raw log
Run id_segregation.py to extract structured CAN/DNP3 frames.

Compute baseline ratios
Use ratio_calculation.py on clean data to generate time-windowed ratio files.

Apply RUC algorithm
Execute setup_ruc_data.py to compute RUC residuals for various kappa and frame lengths.

Evaluate FA/MD trade-offs
Run ruc_cv_fa_md.py for model validation and threshold testing.

Create on–off test scenarios
Generate alternating benign/attack sequences using on_off_testset.py.

Performance benchmarking
Use on_off_perform_ev.py to assess time to detection and robustness across test files.

⚙️ Requirements

Python 3.8 or higher

Dependencies:

pip install pandas numpy matplotlib glob2

▶️ How to Run

Example end-to-end sequence:

python id_segregation.py
python ratio_calculation.py
python setup_ruc_data.py
python ruc_cv_fa_md.py
python on_off_testset.py
python on_off_perform_ev.py


Ensure all required CSV datasets are in the same working directory.
