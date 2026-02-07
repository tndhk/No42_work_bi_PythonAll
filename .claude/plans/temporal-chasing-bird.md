# Fix: HAMM Overview video_duration 文字列→数値変換エラー

## Context

HAMM Overviewダッシュボードで Volume Table / KPIカードの表示時にエラーが発生。
`video_duration`カラムが "HH:MM:SS" 形式の文字列のままDataFrameに読み込まれており、
KPI計算で `.mean()` を呼ぶと文字列連結→数値変換失敗でクラッシュする。

## 根本原因

- `_prepare_base_df()` (`_data_loader.py:47-61`) で `video_duration` カラムの型変換が未実装
- `_callbacks.py:336` の `df[COLUMN_MAP["video_duration"]].mean()` が文字列Seriesに対して呼ばれ失敗

## 修正方針

### Step 1: `_data_loader.py` - `_prepare_base_df()` に video_duration の秒数変換を追加

ファイル: `src/pages/hamm_overview/_data_loader.py`（47-61行付近）

`_prepare_base_df()` 内で `pd.to_timedelta()` を使い "HH:MM:SS" 文字列を秒数（float）に変換する。
内部計算用に `_video_duration_seconds` 派生カラムを追加し、元の文字列カラムはTask Tableの表示用に保持する。

```python
dur_col = COLUMN_MAP["video_duration"]
df["_video_duration_seconds"] = pd.to_timedelta(df[dur_col], errors="coerce").dt.total_seconds()
```

### Step 2: `_callbacks.py` - KPI計算を秒数カラム参照に変更

ファイル: `src/pages/hamm_overview/_callbacks.py`（336行付近）

`.mean()` の対象を `_video_duration_seconds` カラムに変更。
表示フォーマットは秒数→ "MM:SS" 形式に変換。

```python
avg_seconds = df["_video_duration_seconds"].mean()
if pd.isna(avg_seconds):
    avg_duration_str = "N/A"
else:
    mins, secs = divmod(int(avg_seconds), 60)
    hrs, mins = divmod(mins, 60)
    avg_duration_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
```

### Step 3: Task Table の表示は変更なし

`_build_task_table()` (145行) は元の `video_duration` 文字列カラムをそのまま "Source File Duration" として表示しており、変更不要。

## 影響ファイル

| ファイル | 変更内容 |
|---|---|
| `src/pages/hamm_overview/_data_loader.py` | `_prepare_base_df()` に秒数変換を追加 |
| `src/pages/hamm_overview/_callbacks.py` | KPI計算を秒数カラムから算出 + 表示フォーマット修正 |

## 検証方法

1. `python3 -c "import src.pages.hamm_overview._data_loader"` でインポートエラーがないことを確認
2. アプリ起動後、HAMM OverviewページでエラーなくテーブルとKPIが表示されることを確認
3. KPIの "Average Video Duration" が "HH:MM:SS" 形式で妥当な値を表示することを確認
