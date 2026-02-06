# 開発者ガイド (CONTRIB)

最終更新: 2026-02-06

## このドキュメントについて

- 役割: 開発者向けクイックスタートガイド、開発コマンド、プロジェクト構造の説明
- 関連: 技術仕様は [tech-spec.md](tech-spec.md) を参照

---

## 1. 前提条件

| ツール | バージョン |
|--------|-----------|
| Docker / Docker Compose | 最新安定版 |
| Python | 3.9+ |

---

## 2. クイックスタート

```bash
# 1. 環境変数ファイル作成
cp .env.example .env

# 2. 全サービス起動
docker compose up --build
```

| サービス | URL | 説明 |
|---------|-----|------|
| Dashアプリ | http://localhost:8050 | Plotly Dashダッシュボード |
| MinIO Console | http://localhost:9001 | S3互換ストレージ (admin: minioadmin/minioadmin) |

> docker-compose設定の詳細は `docker-compose.yml` を参照

---

## 3. 環境変数

`.env.example` を `.env` にコピーして設定。

### 環境変数一覧

| カテゴリ | 変数名 | デフォルト値 | 説明 |
|---------|--------|-------------|------|
| S3 | `S3_ENDPOINT` | `http://localhost:4566` | S3エンドポイント（ローカル開発時はMinIO） |
| S3 | `S3_REGION` | `ap-northeast-1` | S3リージョン |
| S3 | `S3_BUCKET` | `bi-datasets` | Datasetバケット名 |
| S3 | `S3_ACCESS_KEY` | `test` | S3アクセスキー（ローカルのみ） |
| S3 | `S3_SECRET_KEY` | `test` | S3シークレットキー（ローカルのみ） |
| 認証 | `BASIC_AUTH_USERNAME` | `admin` | Basic認証ユーザ名 |
| 認証 | `BASIC_AUTH_PASSWORD` | `changeme` | Basic認証パスワード |

---

## 4. 開発コマンド

### Python開発

| コマンド | 説明 |
|---------|------|
| `python app.py` | Dashアプリ起動（開発モード） |
| `pytest` | テスト実行 |
| `pytest --cov=src` | カバレッジ付きテスト |
| `pytest -v -k "test_name"` | 特定テストのみ実行 |
| `ruff check src/` | リンティング |
| `ruff format src/` | フォーマット |
| `mypy src/` | 型チェック |

### Docker Compose

| コマンド | 説明 |
|---------|------|
| `docker compose up --build` | 全サービス起動 |
| `docker compose up -d --build` | バックグラウンド起動 |
| `docker compose down` | 停止 |
| `docker compose down -v` | 停止 + データ削除 |
| `docker compose logs -f dash` | Dashアプリログ確認 |
| `docker compose logs -f minio` | MinIOログ確認 |

---

## 5. テスト

### テスト基準

| コンポーネント | 基準 |
|---------------|------|
| Python | pytest pass |

### テスト実行

```bash
# 仮想環境で実行
source .venv/bin/activate
pytest

# カバレッジ付き
pytest --cov=src --cov-report=html
```

---

## 6. コーディング規約

### Python

- フォーマッタ/リンタ: Ruff (line-length: 100, target: py39)
- 型チェック: mypy (strict, 一部 allow_untyped_defs)
- 命名: snake_case (変数/関数), PascalCase (クラス)
- テスト: pytest

---

## 7. Git ワークフロー

### ブランチ命名

- `feature/xxx` - 機能開発
- `fix/xxx` - バグ修正
- `docs/xxx` - ドキュメント
- `refactor/xxx` - リファクタリング

### コミットメッセージ

```
<type>: <summary>

<body (optional)>
```

type: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### PR前チェック

```bash
# Python
ruff check src/ && mypy src/ && pytest --cov=src
```

---

## 8. プロジェクト構造

```
No42_work_bi_PythonAll/
├── app.py                    # Dashアプリエントリーポイント
├── requirements.txt          # 依存パッケージ
├── .env.example             # 環境変数テンプレート
├── docker-compose.yml       # Docker Compose設定
├── Dockerfile.dev           # 開発用Dockerfile
├── pyproject.toml          # pytest/ruff/mypy設定
└── src/
    ├── __init__.py
    ├── auth/                # 認証
    │   └── basic_auth.py   # Basic認証設定
    ├── data/               # データ層
    │   ├── config.py      # 設定管理
    │   ├── s3_client.py   # S3クライアント
    │   ├── parquet_reader.py  # Parquet読み込み
    │   ├── csv_parser.py   # CSV解析
    │   ├── type_inferrer.py   # 型推論
    │   ├── dataset_summarizer.py  # データセット統計
    │   └── models.py      # データモデル
    ├── charts/             # チャート
    │   └── templates.py   # チャートテンプレート
    ├── core/               # コア機能
    │   └── logging.py     # ログ設定
    ├── exceptions.py      # カスタム例外
    ├── layout.py          # Dashレイアウト
    └── callbacks.py       # Dashコールバック
```

---

## 9. 主要依存パッケージ

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| dash | >=2.14.0 | Webフレームワーク |
| dash-bootstrap-components | >=1.5.0 | Bootstrap UIコンポーネント |
| dash-auth | >=2.0.0 | Basic認証 |
| pandas | >=2.0.0 | データフレーム処理 |
| pyarrow | >=14.0.0 | Parquet読み書き |
| boto3 | >=1.34.0 | AWS SDK (S3) |
| plotly | >=5.0.0 | 可視化 |
| chardet | >=5.0.0 | エンコーディング検出 |
| numpy | >=1.24.0 | 数値計算 |
| structlog | >=23.0.0 | 構造化ログ |
| python-dotenv | >=1.0.0 | 環境変数管理 |
| pydantic-settings | >=2.0.0 | 設定管理 |

---

## 10. 関連ドキュメント

| ドキュメント | 内容 |
|-------------|------|
| `docs/tech-spec.md` | 技術仕様書 |
| `CLAUDE.md` | プロジェクト開発メモ |
