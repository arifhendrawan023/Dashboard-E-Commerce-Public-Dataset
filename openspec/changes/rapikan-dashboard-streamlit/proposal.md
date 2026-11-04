# Proposal

## Why

`dashboard.py` is the interactive delivery medium for the e-commerce analysis, but it currently cannot be relied on to run locally: Streamlit is not installed and no dependency manifest exists, and the code carries latent compatibility and robustness problems (seaborn 0.13 `palette`-without-`hue` deprecation, deprecated `st.sidebar.image(width=...)`, an unhandled `NaN` segment in the RFM groupby, and matplotlib figures that are never closed). The file's own section comments describe a clear two-analysis structure, but several details drift from what those comments promise. The dashboard must be tidied, made faithful to its documented structure, and guaranteed to run error-free on a fresh local machine.

## What Changes

- Reorganize `dashboard.py` so each section matches its own banner comments (`LOAD DATA`, `SIDEBAR FILTER`, `HEADER UTAMA`, `BAGIAN 1: PERTANYAAN 1`, `BAGIAN 2: PERTANYAAN 2 (RFM)`).
- Fix compatibility and robustness defects so the app runs without errors or noisy warnings:
  - seaborn `barplot` calls: remove hue-less `palette` usage that triggers FutureWarning under seaborn 0.13.
  - Replace deprecated `st.sidebar.image(..., width=...)`.
  - Handle the `NaN`/empty `Segment` group in the RFM aggregation instead of relying on silent `dropna`.
  - Close matplotlib figures after rendering to avoid figure-accumulation warnings.
- Keep both analytical sections working end-to-end: (1) top-10 longest-delivery product categories annotated with review score and total orders; (2) RFM segment customer-count and revenue bar charts, each with its insight box.
- Add a `requirements.txt` pinning the runtime dependencies so the app installs and runs locally.
- Add a short `README.md` with setup and `streamlit run dashboard.py` instructions.

Out of scope: new analytical questions beyond the two documented sections, and changes to the `main_data.csv` / `rfm_data.csv` data files.

## Capabilities

### New Capabilities
- `ecommerce-dashboard`: the interactive Streamlit dashboard that loads the prepared e-commerce datasets, lets the user filter by analysis year, and presents the delivery-time-vs-satisfaction and RFM customer-segmentation analyses with their insights.

### Modified Capabilities
<!-- None: no existing specs, and no pre-existing capability requirements are changing. -->

## Impact

- **Code**: `dashboard.py` (restructure + fixes).
- **New files**: `requirements.txt`, `README.md`.
- **Data**: reads `main_data.csv` (columns: `order_purchase_timestamp`, `product_category_name`, `delivery_days`, `review_score`) and `rfm_data.csv` (columns: `customer_unique_id`, `Recency`, `Frequency`, `Monetary`, `Segment`). No data files change.
- **Dependencies**: `streamlit` (currently not installed in the environment), `pandas`, `numpy`, `matplotlib`, `seaborn`.
- **Runtime**: Python 3.12; local launch via `streamlit run dashboard.py`.
