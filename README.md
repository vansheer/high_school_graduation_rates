#### Project 5: Social Impact Group Work
Anel Akiyanova, Luke Heeringa, Yang Xu (Van)

Data Science Immersive Remote (DSIR-113020)

February 11, 2021

---

#### Problem Statement

The purpose of this work was to determine what features are most impactful in predicting high school graduation rates. Primary audience of the project is state and local governments, as well as, federal government, and education non-profit organizations. 

#### Executive Summary

The predicted target feature is the 4-year (on time) high school graduation rate of a school district’s 2018 graduating class. In preliminary research we found that on the state level, three-quarters of states have graduation rates between 80 and 90%. In 2018, Iowa was the state with the highest graduation rate of 91%, and the District of Columbia had the lowest graduation rate of 69%. In our analysis, charter-only districts were found to have an average graduation rate of 72%, while mixed charter and non-charter districts had an average of 80% graduation rate, and fully non-charter school districts had the highest average at 90% graduation rate. Although academic success and graduation is influenced by a myriad of social, geo-political, and community economic factors, this team chose to focus on school finances as a numeric proxy for larger issues of inequity.  

Data was primarily sourced from the National Center for Education Statistics (NCES), who publish annual financial statements for every US public school district. Because the NCES no longer publishes national listings of outcomes like graduation rate, however, their data had to be supplemented with state-level publications of graduation rate by school district. Each state’s files are formatted slightly different and are available in varying levels of granularity, so each had to be read in individually and standardized before being able to match school districts by name with their finances as given by the NCES. 

Graduation rate may remain unpublished if student population is insufficiently large, so not every district’s graduation rate could be included. Additionally, some states only require districts to report whether their cohorts fell into certain ranges of graduation rate, such as above 95% or below 5%. With this restriction, all school districts with a graduation rate greater than or equal to .95 were set to be .95, and all school districts with a graduation rate less than or equal to .05 were set to be .05. Any other rate ranges were set to their midpoint (i.e. a school district with a graduation rate of “80-90%” was set equal to .85).

School districts’ fall memberships (the number of students enrolled at the beginning of the 2017-2018 school year) ranged between less than 10 to greater than 600,000, but primarily consisted of districts with between 1,000 and 2,000 students. The distributions of district size and most financial features were heavily skewed, clustering near the bottom of the range with long right tails consisting of the most populous and funded districts. To account for the skew in distribution, all financial features were scaled to be in proportion with the school district size by dividing by the fall membership. Any school district listed with a fall membership of zero or less was dropped from the dataset.

Representing finances as per student moved to somewhat normalize the distributions, but they tended to still be right-skewed, so features were then set to be the log (base 10) of the per student calculations. Features with values of zero or below were determined to represent incomplete data for the district, and were set to be the simple mean of their column values to prevent errors when finding the log. Log-scaling values allowed the modeling process to better examine the full range of values, essentially stretching out the bottom end of the distribution and shortening the top. This both dampens the effect of outliers and magnifies variance within the most heavily-clustered sections of the distributions. 

**Feature Selection**

In our dataset, we were dealing with 133 different variables and the way we wanted to structure the  process is to break the features down into categories to better understand how each variable is correlated and how variables are correlated to the target (please see data dictionary for more details). The data was primarily fiscal and included a good amount of financial indicators per school district. For example, breakdown of State and Local revenue streams, detailed look at expenditures, spendings on salaries to instructional and business teams, as well as, details on school district assets and debt. 

We’ve also done background research on 2018 spending per student split by state. On average, schools spent $12,612 per pupil, annually. At the top of the range is State of New York with $24,040 annual spendings, followed by Connecticut and New Jersey with around $20,000 each. Utah is at the other end of the range with $7,628 annual spendings. The federal government provides ~8% of funding for public education; state and local governments provide ~47% and ~46% of public education funds, respectively. The funding amount is correlated to local property taxes leading to a disbalance between wealthy and impoverished school districts and even different schools within a single school district. 
  
We’ve noticed multicollinearity between the variables early on in the process. Decided that we will avoid linear models as multicollinearity normally weakens statistical power of linear regressors. For our final modeling purposes, we dummified categorical features and used 33 predictors (please see data dictionary for more details). 

**Model Comparison**

Please see a comparison of the six different regressors that we employed in this work along with the baseline model (for details, please see models folder). Our top performing model was Random Forest Regressor with r2-score 0.72, implying that the model explains 72% of the variance of the data it hasn’t yet seen and RMSE 0.07. That compares to the Null Model r2-score 0 and RMSE 0.13. For the baseline model, we used the mean value of the y-variable as our predictions. 
 
We tested linear regression - as anticipated, the model's performance was affected by high correlation between features.

| Model | R2-score | RMSE |
| ------|----------|------|
| Null Model | 0.00 | 0.13 |
| Random Forest Regressor | 0.72 | 0.07 |
| Bootstrap Aggregation | 0.67 | 0.07 |
| Gradient Boosting | 0.47 | 0.09 |
| SVR | 0.35 | 0.10 |
| Neural Network | 0.31 | 0.10 |
| AdaBoost Regressor | 0.12 | 0.11 |

**RFE**

In order to get details on what features were most impactful, we employed several methods. One of the algorithms that we used was Recursive Feature Elimination (RFE) (for details, please see notebook_1_random_forest.ipynb in the models folder). Here is the list of all features that RFE ranked as most important:

- Teacher Salaries - support services - pupils
- Salaries - Instruction
- No associated schools are charter
- Total Federal Revenue
- Local Revenue - District Activity 
- Total Expenditures
- Other Funds
- Textbooks
- Teacher Salaries - special education
- Teacher Salaries - other education
- Teacher Salaries - regular programs
- Teacher Salaries - support services - instructional staff
- Salaries - School Admin
- Salaries - business/ other
- Employee Benefits - instruction
- Employee benefits - support services - pupils
- Total State Revenue

**Principal Component Analysis**

Another tool that we employed to assess feature importance was Principal Component Analysis (PCA). This is a large dataset and we wanted to reduce dimensionality, to be able to analyze the results of the model, while preserving as much information as possible. Principal components are constructed as a combination of the initial features, so that most of the information within the initial features is compressed into the first components and represent maximum variance. Looking at the first ten principal components, we discovered that these variables carried most weight (for details, please see notebook_1_random_forest.ipynb in the models folder):

- Some but not all associated schools are charter
- No associated schools are charter
- Total Federal Revenue
- Total State Revenue
- Local Revenue - District Activity 
- Local Revenue - Textbook Sales
- Local Revenue - Fines and Forfeits
- Local Revenue - Individual and Corporate Income Taxes
- Teacher Salaries - Vocational Ed programs
- Teacher Salaries - support services - instructional staff
- Salaries - School Admin
- Salaries - business/ other
- Employee benefits - support services - instructional staff
- Employee benefits - support services - school admin
- Sinking Fund
- Other Funds
- Long term debt outstanding at beg of year
- Long terms debt - issued during fiscal year
- Long term debt outstanding at end of year
- Short term debt outstanding at beg of year

**App Predicting Graduation Rate**

We built a simple web app with Streamlit for users who would like to access graduation information in a visualized way. The app lets users select a state and a school district, then display the map of that district based on the geographic coordinates pulled with Geopy. A marker is placed on the map to identify the school district. Users can move their mice over the mark to see the name of the school district and its real-world graduation rate. 

Five numeric features that are on top of the list of importance are displayed below the map, where each one is in the form of a slider so the values of these features can be altered. A real-time prediction will be performed in the backend upon each value change, and users can see how different input might change the final result. 

The result, of course, is affected by many more features than the five listed. We only include these five numeric ones so that users can play around and get a sense of where they can possibly focus on. There are also many categorical features one needs to consider, such as whether it's a charter school district or not. To further improve the readability, a bar plot of the real-world rate and the predicted rate can be included.

#### Key Findings and Recommendations

Based on the model and our work on feature analysis, we recommend focusing and investing in the features listed below in an attempt to improve graduation rates. The features consistently proven to be strong predictors of the output using both Recursive Feature Elimination and Principal Component Analysis methods. 

- Total Federal Revenue
- Total State Revenue
- Local Revenue - District Activity 
- Teacher Salaries - support services - instructional staff
- Salaries - School Admin
- Salaries - business/ other
- Employee benefits - support services - school admin
- School Funds

For future research, we would incorporate non-fiscal variables in our work to make the analysis more comprehensive. We would particularly be interested in looking at student participation and attendance, student academic performance and achievements, teacher labor union data.

#### File Directory

- README.md 

- sources.md : a linked listing of the sources used in background research and data collection

- cleaning/
    - 01_cleaning_code_by_state/
        - {ABBR}_cleaning.ipynb : code for merging data from the state denoted by abbreviation {ABBR}
    - 02_state_merging.ipynb : code to merge all state-level files into a single national file
    - 03_fullset_cleaning.ipynb : code standardizing names, removing duplicates, and dropping unneeded features
    - 04_log_per_student.ipynb : code to transform the national dataset logarithmically and by individual school district size
    - 05_geo_merging.ipynb : code merging the included school districts with their geographic location given by the NCES directory


- data/
    - state_data_raw/
        - {statename}{20XX}.{ext} : raw state-level district graduation data in .csv, .pdf, .txt, .xls, or .xlsx form; {statename} indicates the state, {20XX} indicates the graduation year of the data, unless the data is for mulitple years, in which case no year will be indicated
    - state_data_merged/
        - {ABBR}.csv : merged data for the state denoted by abbreviation {ABBR} generated from corresponding {ABBR}_cleaning.ipynb file in cleaning/01_cleaning_code_by_state/
    - fiscal2018 : raw SAS format file from NCES of school district financials for the school year 2017-2018
    - directory.csv : raw NCES file of school district locations
    - 50_states.csv : merged data from the files in /state_data_merged/
    - dataset.csv : cleaned version of 50_states.csv
    - log_per_student.csv : transformed version of dataset.csv
    - grad_rate_by_zip.csv : zip code lookup data file created by merging dataset.csv and directory.csv


- EDA/
    - plots/
        - {var}_hist.png : histogram showing the initial distribution of variable {var}
        - percap_{var}_hist.png : histogram showing the per student distribution of variable {var}
        - log_{var}_hist.png : histogram showing the log-transformed per student distribution of variable {var}
        - log_{var}_scatter.png : scatter plot showing the relationship between the log-transformed per student variable {var} and the target variable ‘graduation rate’
    - presentation_plots/
        - district_size.png : a seaborn-generated version of the distribution of variable ‘v33’ (fall membership) included in the presentation slides
        - totalrev.png : a seaborn-generated version of the initial distribution of variable ‘totalrev’ included in the presentation slides
        - totalrev_percap.png : a seaborn-generated version of the per student distribution of variable ‘totalrev’ included in the presentation slides
        - totalrev_log.png : a seaborn-generated version of the log-transformed, per student distribution of variable ‘totalrev’ included in the presentation slides
    - 01_eda_initial.ipynb : exploration, analysis, and plot-generating code of the pre-transformation data in dataset.csv
    - 02_eda_transformed.ipynb : exploration, analysis, and plot-generating code of the transformed data in log_per_student.csv
    - presentation_visuals.ipynb : short notebook with code used to generate the visuals in /presentation_plots/


- models/
    - notebook_1_random_forest.ipynb: variable heatmap, null model, random forest regression, RFE, PCA results
    - notebook_2_svr.ipynb: support vector regression results
    - notebook_3_gradientboosting.ipynb: gradient boosting regression results
    - notebook_4_bagging.ipynb: bootstrap aggregation results
    - notebook_5_adaboost.ipynb: adaboosting regression results
    - notebook_6_neural_network.ipynb: neural network regression results
    
    
- streamlit/
    - data/
        - states/
            - zip/
                - state_abbreviation.csv
            - states_lanlon
        - dataset.csv
        - full_school_district_with_zip.csv
    - models/
        - random_forest
    - notebooks/
        - district_address_mapping.ipynb
        - geocoding_test.ipynb
    - project5.py

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

See sources.md

---
