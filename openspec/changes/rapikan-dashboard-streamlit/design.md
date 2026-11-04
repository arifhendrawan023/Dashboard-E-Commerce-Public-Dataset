# Design

## Context

See `proposal.md - Why` for motivation. Current constraints that shape the approach:

- Single-file Streamlit app (`dashboard.py`) with a documented section structure defined by its own banner comments.
- Environment is Python 3.12 with pandas 3.0.3, numpy 2.4.6, matplotlib 3.11.0, and seaborn 0.13.2. Streamlit is not installed.
- Data is already prepared: `main_data.csv` (110,839 rows) and `rfm_data.csv` (85,578 rows), where `rfm_data.csv` contains a small number of `NaN` `Segment` values.
- The existing code already implements both analyses; the work is tidying, fixing, and packaging, not redesigning.

## Goals / Non-Goals

**Goals:**
- Every section of `dashboard.py` matches its banner comment and runs without exceptions or deprecation warnings.
- Deterministic, readable charts (stable segment ordering, readable annotations).
- A fresh machine can install and run the dashboard from the repository alone.

**Non-Goals:**
- Adding analytical questions, pages, or navigation beyond the two documented sections.
- Changing the prepared datasets or their schema.
- Containerization, deployment, or CI configuration.

## Decisions

**Keep matplotlib + seaborn for charting, rather than Streamlit-native charts.**
The existing file and the referenced practice material use matplotlib/seaborn, so keeping them preserves visual parity and the annotation logic (per-bar text). *Alternative:* Streamlit `st.bar_chart`/Altair — rejected because it duplicates library changes and loses direct per-bar annotation control.

**Resolve the seaborn 0.13 hue-less `palette` warning explicitly.**
In seaborn 0.13, passing `palette` without `hue` emits a `FutureWarning`. Assign `x`/`y` to a color role via `hue` with `legend=False`, or set `color`/`palette` per the current seaborn contract, so both charts render cleanly. *Alternative:* pin seaborn below 0.13 — rejected (downgrading to silence a warning).

**Drop rows with a missing `Segment` before the RFM aggregation and fix segment order.**
`rfm_data.csv` contains `NaN` segments. Aggregate on `Segment` after excluding missing values, and order categories explicitly as `Low → Mid → High → VIP` when present, so both RFM charts show a consistent, meaningful order. *Alternative:* rely on groupby `dropna` and seaborn's default order — rejected because ordering would be alphabetical and the intent is segment progression.

**Close each matplotlib figure after `st.pyplot`.**
Call `plt.close(fig)` after rendering to prevent figure accumulation across reruns. *Alternative:* leave as-is — rejected because of repeated-rerun leaks.

**Pin runtime dependencies in `requirements.txt` to the tested versions.**
Record the versions validated locally (streamlit, pandas, numpy, matplotlib, seaborn) so the environment is reproducible. *Alternative:* unpinned requirements — rejected for reproducibility.

**Keep the year filter as the single sidebar filter.**
The comments and the two analyses only require a year selector; no additional filter is needed. *Alternative:* add category/segment filters — rejected as scope creep.

## Risks / Trade-offs

- **Dependency drift on a fresh install** (unpinned transitive deps) → pin direct deps to the versions validated here and note the requirement in the README.
- **Newer pandas 3.0 string dtype behavior** around groupby/aggregation could differ from older pandas → validate the app by running it, not just by reading the code.
- **Small-sample categories** (e.g. categories with a single order) can distort the "longest delivery" top-10 → keep the existing note in the delivery insight so readers do not over-interpret.

## Migration Plan

Local-only change; no data or schema migration. Rollback is reverting `dashboard.py`, `requirements.txt`, and `README.md`. Verification: `pip install -r requirements.txt` then `streamlit run dashboard.py`, confirming both sections render without errors or warnings.
