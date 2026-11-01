# F1競輪データ（2025年以降）

F1開催の **A級1・2班 / S級** を横断して参照・検証する専用リポジトリ。
元データを変更せず、`yuhevita-wq/keirin-market-analysis-` にある一次保存ファイルを利用します。

## 原本の所在（2026-11-01確認）

| 区分 | 収録範囲 | 原本 |
| --- | --- | --- |
| S級 | 2025-01-01〜2025-12-31（四半期別） | [2025 S級F1全レース](https://github.com/yuhevita-wq/keirin-market-analysis-/tree/main/data/2025/s_class_f1_all_parts) |
| S級 | 2026-01-01〜2026-06-30 | [2026上半期S級](https://github.com/yuhevita-wq/keirin-market-analysis-/tree/main/data/2026_h1/s_class_f1_all) |
| S級 | 2026-07-01〜2026-08-30 | [2026夏季S級](https://github.com/yuhevita-wq/keirin-market-analysis-/tree/main/data/2026_future_block1/s_class_f1_20260701_20260830) |
| A級1・2班 | 2025-01-01〜2026-10-02（2か月別・末尾は部分期間） | [A級1・2班](https://github.com/yuhevita-wq/keirin-market-analysis-/tree/main/data/a_class_12) |

### 必ず守る区分

- **F1だけを使用**：S級の一次データは開催種別がF1。A級データは **F1とF2が混在** しているため `meeting_grade=F1` を必須とする。
- A級は **A1・A2** を対象とし、A3やガールズは混ぜない。
- 車立ては **5・6・7車を含み、7車立て限定にはしない**。必要なら `entry_count=7` で抽出する。
- `data/all_classes/` は元フォルダーの整理用コピーであり、**別原本として二重に取り込まない**。
- `data/2025/s_class_yosen` はF1全レースと重複するため併合しない。
- `race_id`、`race_id+car_no` で重複検査し、推測補完をしない。

## データの使い方

`data/source_manifest.json` に上記の原本パスと**固定コミット**を記録します。

```bash
# インターネット接続があるPC/GitHub Actionsで原本から取得・再構築
python scripts/build_f1.py --year all

# 生成された年別SQLiteを検索（圧縮版しかない場合は自動展開）
python scripts/query_f1.py --year 2025 --sql "SELECT f1_class, COUNT(*) FROM races GROUP BY f1_class"

# F1・7車立ての3連単払戻データを取得
python scripts/query_f1.py --year 2025 --sql "SELECT r.race_date,r.track,r.race_no,p.combination,p.payout_yen FROM races r JOIN v_paid_trifecta p ON p.race_id=r.race_id WHERE r.entry_count='7' LIMIT 20" --output results.csv
```

- `races`: 日付・競輪場・レース種別・開催種別・ライン予想
- `entries`: 車番別出走表（級班・得点・選手情報）
- `results`: 着順等の結果（**事後**）
- `payouts`: 払戻（**事後**）
- `v_pre_race_races`, `v_pre_race_entries`, `v_paid_trifecta`: 検索用ビュー
- `data/ready/f1_YYYY.sqlite.gz`: 年別の読み取り用データベース（ビルド後）
- `reports/ingestion/YYYY.json`: 取込件数、原本SHA-256、重複・参照整合性・欠損監査（ビルド後）

GitHub Actionsの **Build F1 2025+ datasets** を使うと、年別SQLiteの構築と保存を実行できます。

## データの欠落・注意点

2026-11-01時点、**2026-08-31以降のS級**、**2026-10-03以降のA級** のF1原本は上記の主要保存先には確認できていません。未収録を「レースがなかった」と判断しないでください。原本の期間を超えたデータは生成しません。

S級原本には3連単・3連複の「確定オッズ」がある期間もありますが、本データベースの初期版は **出走表・着順・払戻** に対象を限定しています。A級のオッズを補完しません。確定オッズは締切前に見えた値とは限りません。並びは公開予想であり公式な確定ラインではありません。

公開収集データを過去に遡って取得した時点と当日の出走前情報が完全一致する保証はないため、予測時点の厳密な検証には別途監査が必要です。
