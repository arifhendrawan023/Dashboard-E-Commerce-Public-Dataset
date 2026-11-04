# Spec Delta

## Purpose

An interactive Streamlit dashboard that loads the prepared e-commerce datasets and presents delivery-time-versus-satisfaction and RFM customer-segmentation analyses so the results can be explored and understood by non-technical readers.

## ADDED Requirements

### Requirement: Local launch and declared dependencies
The dashboard SHALL run locally via `streamlit run dashboard.py`, and the project MUST declare its Python runtime dependencies in a `requirements.txt` so a fresh environment can install everything needed to start without a `ModuleNotFoundError`.

#### Scenario: Fresh environment install
- **WHEN** a user installs dependencies from `requirements.txt`
- **THEN** `streamlit`, `pandas`, `numpy`, `matplotlib`, and `seaborn` are available

#### Scenario: Application starts without error
- **WHEN** the user runs `streamlit run dashboard.py`
- **THEN** the app renders the page without raising an exception

### Requirement: Dataset loading
The dashboard SHALL load `main_data.csv` and `rfm_data.csv`, parse the `order_purchase_timestamp` column to a datetime type, and cache the loaded datasets so repeated interactions do not re-read the files.

#### Scenario: Both datasets loaded and typed
- **WHEN** the app runs
- **THEN** both datasets are read and `order_purchase_timestamp` is a datetime column

#### Scenario: Cached across reruns
- **WHEN** the user interacts with a widget and Streamlit reruns the script
- **THEN** the datasets are served from cache instead of being read from disk again

### Requirement: Sidebar filters
The dashboard SHALL present a sidebar containing a year selector populated from the distinct years present in the main dataset, and SHALL restrict the main dataset to the selected year for the delivery analysis.

#### Scenario: Years offered
- **WHEN** the sidebar renders
- **THEN** the selector lists each distinct year found in `order_purchase_timestamp` in ascending order with one year selected by default

#### Scenario: Year filter applied
- **WHEN** a year is selected
- **THEN** the delivery analysis uses only rows whose purchase timestamp falls within that year

### Requirement: Delivery time versus satisfaction analysis
The dashboard SHALL display a chart of the 10 product categories with the longest average `delivery_days` for the selected year, ordered longest-first, and SHALL annotate each bar with that category's average `review_score` and total order count.

#### Scenario: Top 10 categories by delivery time
- **WHEN** the delivery analysis renders for a selected year
- **THEN** exactly the 10 categories with the highest mean `delivery_days` are shown, sorted in descending order

#### Scenario: Per-bar annotation
- **WHEN** the chart is displayed
- **THEN** each bar shows the category's mean `review_score` and its total order count

### Requirement: RFM customer segmentation visualization
The dashboard SHALL present RFM results grouped by `Segment`, showing the number of customers and the total monetary value per segment, and SHALL render the charts without error when records have a missing segment value.

#### Scenario: Customer count per segment
- **WHEN** the RFM section renders
- **THEN** a chart shows the number of customers for each segment

#### Scenario: Revenue per segment
- **WHEN** the RFM section renders
- **THEN** a chart shows the total monetary value for each segment

#### Scenario: Missing segment tolerated
- **WHEN** some records have a missing or `NaN` segment value
- **THEN** the dashboard still renders the RFM charts without raising an error

### Requirement: Analytics insight callouts
The dashboard SHALL display, for each analytical section, an insight callout summarizing the key finding of that section.

#### Scenario: Delivery insight shown
- **WHEN** the delivery analysis is displayed
- **THEN** an insight callout describing the delivery-time and review-score relationship is shown

#### Scenario: RFM insight shown
- **WHEN** the RFM analysis is displayed
- **THEN** an insight callout describing segment contribution is shown
