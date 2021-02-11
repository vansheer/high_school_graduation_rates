#### Project 5: Social Impact Group Work
Anel Akiyanova, Luke Heeringa, Yang Xu (Van)

Data Science Immersive Remote (DSIR-113020)

February 11, 2021

---

#### Problem Statement

---

#### Executive Summary



**Model Comparison**

| Model | R2-score | RMSE |
| ------|----------|------|
| Null Model | 0.00 | 0.13 |
| Random Forest Regressor | 0.72 | 0.07 |
| Bootstrap Aggregation | 0.67 | 0.07 |
| Gradient Boosting | 0.47 | 0.09 |
| SVR | 0.35 | 0.10 |
| Neural Network | 0.31 | 0.10 |
| AdaBoost Regressor | 0.12 | 0.11 |


#### Key Findings

---

#### File Directory

- README.md 

- sources.md

- cleaning
    - cleaning_code_by_state
        - {ABBR}_cleaning.ipynb 
    - fullset_cleaning.ipynb
    - geo_merging.ipynb
    - log_per_student.ipynb
    - state_merging.ipynb

- data
    - state_data_raw
        - {statename}20XX.csv
        - {statename}20XX.pdf
        - {statename}20XX.txt
        - {statename}20XX.xls
        - {statename}20XX.xlsx
    - state_data_merged
        - {ABBR}.csv
    - fiscal2018
    - directory.csv
    - 50_states_clean.csv
    - dataset.csv
    - grad_rate_by_zip.csv
    - log_per_student.csv

- EDA
    - plots
        - {var}_hist.png : 
        - percap_{var}_hist.png :
        - log_{var}_hist.png :
        - log_{var}_scatter.png :
    - presentation_plots
        - district_size.png
        - totalrev.png
        - totalrev_percap.png
        - totalrev_log.png
    - eda_initial.ipynb
    - eda_transformed.ipynb
    - presentation_visuals.ipynb

- models
    - notebook_1_random_forest.ipynb
    - notebook_2_svr.ipynb
    - notebook_3_gradientboostin
---

#### Data Dictionary

| Category | Column Name | Description |
| ---------|-------------|-------------|
| School Identification | 2 | Some but not all associated schools are charter |
| School Identification | 3 | No associated schools are charter |
| Revenue | tfedrev | Total Federal Revenue |
| Revenue | tstrev | Total State Revenue |
| Revenue | a13 | Local Revenue - District Activity |
| Revenue | t06 | Local Revenue - Property Taxes |
| Revenue | a11 | Local Revenue - Textbook Sales |
| Revenue | u30 | Local Revenue - Fines and Forfeits |
| Revenue | t40 | Local Revenue - Individual and Corporate Income Taxes |
| Expenditures | totalexp | Total Expenditures |
| Expenditures | v93 | Textbooks |
| Salaries | z33 | Salaries - Instruction |
| Salaries | z35 | Teacher Salaries - regular programs |
| Salaries | Z36 | Teacher Salaries - special education |
| Salaries | z37 | Teacher Salaries - Vocational Ed programs |
| Salaries | z38 | Teacher Salaries - other education |
| Salaries | v11 | Teacher Salaries - support services - pupils |
| Salaries | v13 | Teacher Salaries - support services - instructional staff |
| Salaries | v17 | Salaries - School Admin |
| Salaries | v37 | Salaries - business/ other |
| Employee Benefits | v10 | Employee Benefits - instruction |
| Employee Benefits | v12 | Employee benefits - support services - pupils |
| Employee Benefits | v14 | Employee benefits - support services - instructional staff |
| Employee Benefits | v18 | Employee benefits - support services - school admin |
| Employee Benefits | v24 | Employee benefits - support services - student transportation |
| Employee Benefits | v38 | Employee benefits - supports services - business / other |
| Assets | w01 | Sinking Fund |
| Assets | w31 | Bond Fund |
| Assets | w61 | Other Funds |
| Debt | 19H | Long term debt outstanding at beg of year |
| Debt | 21f | Long terms debt - issued during fiscal year |
| Debt | 41f | Long term debt outstanding at end of year |
| Debt | 61v | Short term debt outstanding at beg of year |

For full list of variables, please see the link (https://nces.ed.gov/ccd/Data/txt/sdf18_1a_layout.txt).

---

#### Citations

---