# Real-Time SaaS Analytics Platform (Interview-ready starter)

This project demonstrates a SaaS usage analytics pipeline with **synthetic demo data**.
It is a local, reproducible prototype—not a live production event-streaming system.

## What it includes
- 6,000 synthetic `user_events` records and 2,500 synthetic `click_events` records.
- Python/Pandas ETL for validation, cleaning, and derived date fields.
- BigQuery loader (optional; requires Google Cloud credentials).
- SQL analytics queries.
- Streamlit dashboard for local interactive visualizations.
- Prepared CSV data for Looker Studio connection.

## Data fields
### user_events
`event_id`, `user_id`, `event_name`, `event_timestamp`, `page_name`, `session_id`, `device_type`, `country`, `subscription_plan`

### click_events
`event_id`, `user_id`, `button_name`, `event_timestamp`, `page_name`, `session_id`, `device_type`, `subscription_plan`

The records are randomly generated for demonstration. Do not represent them as actual customer activity.

## Architecture
Synthetic/demo events -> Python/Pandas cleaning -> CSV outputs -> (optional) BigQuery tables -> SQL analytics -> Streamlit dashboard or Looker Studio.

## Run locally
1. Install Python 3.10+.
2. In the project folder:
   ```bash
   python -m venv .venv
   ```
   Windows:
   ```bash
   .venv\Scripts\activate
   ```
   macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Clean and validate data:
   ```bash
   python scripts/etl.py
   ```
5. Launch dashboard:
   ```bash
   streamlit run app.py
   ```

## Optional: load data to BigQuery
The provided script can create/load tables in your BigQuery dataset. It requires:
- A Google Cloud project with BigQuery API enabled.
- Credentials configured with Application Default Credentials:
  ```bash
  gcloud auth application-default login
  ```
- Edit `scripts/load_bigquery.py` to set your project ID and dataset (defaults are the project/dataset from the user's earlier screenshot).

Run:
```bash
python scripts/load_bigquery.py
```
The loader creates/replaces the two demo tables using the CSV data. Verify your project/dataset/table names before running. This is an optional action and can incur BigQuery costs depending on configuration/usage.

## Looker Studio
For a Looker Studio dashboard, connect to BigQuery:
1. Open Looker Studio and create a report.
2. Add data -> BigQuery.
3. Choose project `saas-realtime-analytics`, dataset `saas_analytics`, then `user_events` or `click_events`.
4. Add scorecards (Users, Events), line chart (events by date), bar chart (event names or clicked buttons), and filter controls (date, plan, country).
5. This demo dataset uses synthetic values, so label it as sample/demo data.

## Suggested dashboard KPIs
- Total events
- Unique users
- Events per day
- Events by type
- Clicks by button
- Activity by device
- Activity by plan
- Activity by country

## Limitations and next steps
- The data is synthetic, not collected from a live SaaS application.
- The current ETL is batch-oriented.
- This is not streaming real-time ingestion. To make it near-real-time, add an event API/collector, Pub/Sub, streaming processing (e.g. Dataflow), and scheduled/continuous BigQuery ingestion.
