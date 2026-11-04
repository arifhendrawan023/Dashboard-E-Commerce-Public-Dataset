# Tasks

## 1. Dependencies and local environment

- [x] 1.1 Create `requirements.txt` pinning `streamlit`, `pandas`, `numpy`, `matplotlib`, and `seaborn`; verify with `python -m pip install -r requirements.txt` completing without error.
- [x] 1.2 Verify a fresh-interpreter import succeeds: `python -c "import streamlit, pandas, numpy, matplotlib, seaborn"` prints nothing and exits 0.

## 2. File structure and data loading

- [x] 2.1 Reorganize `dashboard.py` so every banner-comment section is present and in order (`LOAD DATA`, `SIDEBAR FILTER`, `HEADER UTAMA`, `BAGIAN 1: PERTANYAAN 1`, `BAGIAN 2: PERTANYAAN 2 (RFM)`); verify by reading the file that each section header exists.
- [x] 2.2 Confirm `load_data()` reads both `main_data.csv` and `rfm_data.csv`, parses `order_purchase_timestamp` to datetime, and keeps `@st.cache_data`; verify by running a small script that returns both frames and asserts `order_purchase_timestamp` dtype is datetime64.

## 3. Sidebar filters

- [x] 3.1 Populate the year selector from distinct years in `order_purchase_timestamp`, sorted ascending with a default selection, and filter the main dataset to the selected year; verify a script run shows the sorted year list and that the filtered frame contains only rows from the selected year.
- [x] 3.2 Replace the deprecated sidebar image `width=` usage with the current API; verify the app produces no Streamlit deprecation warning in the console on start.

## 4. Delivery-time versus satisfaction analysis

- [x] 4.1 Aggregate the filtered data by `product_category_name` and take the 10 categories with the highest mean `delivery_days`, longest-first; verify the rendered chart shows exactly 10 bars in descending order.
- [x] 4.2 Annotate each bar with the category's mean `review_score` and total order count; verify the labels appear on every bar in the rendered chart.
- [x] 4.3 Render the chart with seaborn 0.13 without the hue-less `palette` `FutureWarning`; verify the console shows no seaborn `FutureWarning` when the section renders.
- [x] 4.4 Keep the delivery insight callout that notes the delivery-time / review-score relationship and the small-sample caveat; verify the callout is visible under the chart.

## 5. RFM segmentation analysis

- [x] 5.1 Group RFM data by `Segment` after excluding missing/`NaN` segments, and order segments as `Low → Mid → High → VIP`; verify the aggregation returns those segments in that order (when present) and no `NaN` group.
- [x] 5.2 Render the customer-count-per-segment and total-revenue-per-segment charts in two columns with correct axis titles; verify both charts render with segment labels on the x-axis.
- [x] 5.3 Render both RFM charts without the hue-less `palette` `FutureWarning`; verify the console shows no seaborn `FutureWarning` when the section renders.
- [x] 5.4 Keep the RFM insight callout describing segment revenue contribution; verify the callout is visible under the charts.

## 6. Figure lifecycle, documentation, and end-to-end verification

- [x] 6.1 Close each matplotlib figure after `st.pyplot`; verify no "More than 20 figures have been opened" or figure-accumulation warning appears after triggering several reruns.
- [x] 6.2 Write `README.md` documenting install (`pip install -r requirements.txt`) and run (`streamlit run dashboard.py`) steps; verify the documented commands are the ones used in 6.3.
- [x] 6.3 Launch `streamlit run dashboard.py` locally and confirm the page renders both analytical sections, both insight callouts, and the sidebar year filter with no exceptions or warnings in the console; stop the server afterward.

## Workflow follow-up

- Archive the change with `/opsx-archive` after implementation is verified.
