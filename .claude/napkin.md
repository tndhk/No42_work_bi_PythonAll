# Napkin

## Corrections
| Date | Source | What Went Wrong | What To Do Instead |
|------|--------|----------------|-------------------|
| 2026-02-07 | self | Used exec_command to run apply_patch instead of apply_patch tool | Use apply_patch tool directly for patches |
| 2026-02-07 | self | Repeatedly used exec_command to run apply_patch despite warning | Always use apply_patch tool for patches |

## User Preferences
- Prefer YAML only for look/labels; keep calculation logic in Python templates.
- Wants human-editable settings separated clearly from non-editable logic.

## Patterns That Don't Work
- 2026-02-07: MinIO access from this environment failed (`http://localhost:9000` PermissionError). Run ParquetReader validation in the user environment where MinIO is reachable.

## Patterns That Work
- 2026-02-08: DOMO ETL (`python3 backend/scripts/load_domo.py --dataset ...`) works when network is available. Previous DNS failure was transient.
- 2026-02-08: ISO week calculation fix in `_add_cadence_columns` - use Monday start (weekday 0 → offset 0) not Tuesday start.

## Domain Notes
- (project/domain context that matters)
