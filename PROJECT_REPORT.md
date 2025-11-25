# Stock Tracker — Project Report

Date: 2025-11-25

Prepared by: Joseph Jonathan Fernandes, Nihaal Virgincar, Pratik Nayak, Rajivkumar Naik

---

## Project Overview

Stock Tracker is an interactive R Shiny dashboard for analysis of NIFTY 50 stocks. The project provides data ingestion, validation and quality checks, interactive visualization (time-series, candlesticks, volume, correlations), and an integrated regression analysis module that produces forecasts, trend metrics, and downloadable reports.

The application is designed for analysts and traders who want a quick, exploratory workspace with reproducible outputs and exportable artifacts.

## Contributors

- Joseph Jonathan Fernandes — Lead developer, app architecture, regression module
- Nihaal Virgincar — Frontend UI/UX and charting (Plotly) improvements
- Pratik Nayak — Data validation, ETL utilities, test harnesses
- Rajivkumar Naik — Packaging, installer scripts, logging and deployment helper scripts

## Key Features

- Data ingestion from CSV sources (`NIFTY50_all.csv`, `stock_metadata.csv`)
- Data quality and validation dashboard with missing-data analysis and distribution charts
- Interactive charts built with Plotly: line charts, candlestick charts, moving averages, and correlation heatmaps
- Regression analysis module supporting multiple model types (linear, log-linear, polynomial, multiple regression) with:
  - Model summaries, R² and diagnostic metrics
  - Multi-day forecasts and confidence bands
  - Price predictions table with currency formatting
  - Downloadable markdown reports summarizing the analysis
- Defensive logging using `futile.logger` with a custom wrapper to centralize messages and performance metrics
- Installer script to ensure required R packages are present on the host
- Test scripts for targeted verification of the data pipeline and regression outputs

## Architecture and Code Layout

Top-level files and folders:

- `app.R` — Main Shiny UI and server logic
- `regression.R` — Regression engine, prediction generation, helper metrics
- `charts.R` — Plotly chart builders and helpers (price chart, candlesticks, regression overlay)
- `validation.R` — Data quality checks and summary report generation
- `utils.R` — Data loading and helper utilities
- `logger.R` — Logging initialization and wrappers around `futile.logger`
- `assets/style.css` — Application styling for dark theme (custom styles for predictions table)
- `install_packages.R` and `run_app.bat`/`run_with_regression.bat` — Environment setup and launch helpers
- `tests/` (ad-hoc test scripts) — `basic_test.R`, `test_regression_run.R`, `test_quality_report.R`

Design notes:
- UI is built using `shinydashboard` with modular server-side functions.
- Reactive flows: user selects symbol/date range → filtered data used for charts/metrics → regression triggered by explicit button press (`Run Analysis`).
- Plotly charts are composed in `charts.R`; recent fixes ensure trace lengths are matched before adding prediction/confidence traces to avoid Plotly errors.

## Data Model

Primary dataset fields (example):
- `Date` (Date) — trading date
- `Symbol` (string) — stock symbol
- `Open`, `High`, `Low`, `Close` (numeric) — prices
- `Volume` (numeric)
- `Industry` (string) — metadata for grouping/filtering

Data ingestion merges stock timeseries and metadata into `df_raw` then runs `validate_stock_data()` to produce a cleaned `df` when validation succeeds.

## How to Install and Run (Windows)

Prerequisites:
- R 4.1+ (R 4.4.x recommended)
- PowerShell or Command Prompt

Quick start (from project root):

1. Install required packages (run from PowerShell):

```powershell
Rscript -e "source('install_packages.R')"
```

2. Launch the app:

```powershell
# Use the provided batch script (sets up env and runs app)
.\run_app.bat
# or run directly from R
Rscript -e "shiny::runApp('.')"
```

Notes:
- The installer attempts to install `futile.logger`, `broom`, `forecast`, `zoo`, and other dependencies used by the project. On some machines packages built under a different minor R version may display a warning but usually work.

## Regression Module (technical)

- Main function: `perform_linear_regression(data, symbol, days_ahead)` returns a list containing:
  - `model` — fitted `lm` or other model object
  - `model_type` — label of the model used
  - `model_data` — dataframe used to fit the model (dates + features)
  - `predictions` — dataframe with `Date`, `predicted_price`, `lower_bound`, `upper_bound`
  - `trend` — list with `r_squared`, `adjusted_r_squared`, `slope`, `direction`, etc.
  - `metrics` — RMSE, AIC, current price, predicted 30-day price, volatility, uncertainty

- The UI exposes `Run Analysis` which triggers `eventReactive(input$run_regression, ...)` to run the regression and cache results in a reactive variable.
- Charting code (`plot_stock_price_with_regression`) validates trace lengths (recent patch) to prevent Plotly `recycle_columns` errors.

## Data Quality Module

- `validate_stock_data(df)` performs checks and returns structured results: `valid` Boolean, `issues` list, `data` (cleaned) and `summary`.
- `generate_quality_report(validation_result)` produces HTML summarizing issues, missing data, and recommended corrections.
- UI renders `output$data_quality_summary` with `renderUI()` and shows `missing_data_plot` and `data_distribution_plot` derived from `df_raw`.

## Testing and Verification

Included scripts and recommended checks:
- `basic_test.R` — quick sanity checks for data loading and sample chart generation
- `test_regression_run.R` — runs `perform_linear_regression()` for a sample symbol and prints `str()` of the results (useful to confirm fields)
- `test_quality_report.R` — runs validation and prints / saves the generated report for inspection

How to run tests:

```powershell
Rscript tests/test_regression_run.R
Rscript tests/test_quality_report.R
```

## Known Issues (current)

- Data validation may flag issues for certain symbols; when validation fails the app currently falls back to `df_raw` and logs warnings — this can affect model fit quality.
- Plotly trace size mismatch ("tibble columns must have compatible sizes") was observed earlier; fixed by trimming trace vectors to matching lengths in `charts.R` (see recent commit).
- Some packages may be installed under a different R minor version which emits warnings (harmless in most cases but may require reinstalling packages under the exact R version used).

## Recent Fixes and Notes

- Added defensive checks in `regression.R` to return structured error objects instead of NULL when analysis fails.
- Added `log_info()` wrapper in `logger.R` to avoid missing function errors invoked by regression code.
- Updated the predictions DataTable to use numeric columns and `DT::formatCurrency()` for readable currency display.
- Added `assets/style.css` rules targeting `.predictions-table` to lighten table entries on the dark theme per UX feedback.
- Ensured that menu `tabName` for Data Quality matches the `tabItem` name (`data_quality`) so the sidebar link opens the correct tab.

## Security & Data Privacy

- The application reads local CSV data files only; there are no external write operations by default.
- If deploying to a shared server, configure file system permissions to protect the CSV data and logs.

## Deployment Recommendations

- For production deployment, host behind a Shiny Server (open-source or pro) or containerize with a Rocker image and run behind a reverse proxy.
- Use environment-specific configuration in `config.R` (API keys, file paths).
- For scheduled runs (e.g., automated nightly forecasts), extract the regression workflow into a script and run via CRON / Windows Task Scheduler.

## Next Steps and Roadmap

1. Improve data validation: add automatic imputation strategies (interpolation or model-based) with user opt-in.
2. Add model selection and cross-validation UI so users can compare model performance (k-fold CV) interactively.
3. Add export options for charts (PNG/SVG) and extend report downloads to include CSV of predictions and full diagnostic plots.
4. Add authentication/authorization for multi-user deployments.
5. Add unit tests and CI integration to validate package installation and basic app startup on push.

---

If you want, I can:
- Add this file to source control and commit it with a concise commit message.
- Generate a shorter `README.md` derived from the report for project front-page use.
- Produce a PDF export of this report.

