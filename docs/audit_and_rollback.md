# Audit Trail & Configuration Rollback Procedures

## 1. Audit Logging Policy
Every search query, user ID, permission filter, candidate list, evidence score, recommendation, latency, and user feedback is recorded into the SQLite `search_logs` and `feedback` tables.

## 2. Ranking Configuration Versioning & Rollback
Ranking formulas are version-controlled in JSON configuration files (`ranking_config_v1.json`, `ranking_config_v2.json`) and tracked in the `ranking_configs` database table.

### Rollback Procedure
If a new ranking configuration version (e.g. `v2.0.0`) decreases retrieval quality:
1. Re-point active configuration in `.env` to `src/config/ranking_config_v1.json`.
2. Send HTTP POST to API endpoint `/ranking-config` with version `1.0.0` weights.
3. Verify active config in database:
   ```sql
   UPDATE ranking_configs SET is_active = 0;
   UPDATE ranking_configs SET is_active = 1 WHERE version = '1.0.0';
   ```
