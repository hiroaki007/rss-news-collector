# RSS News Collector

個人開発の学習プロジェクトとして、RSS収集からデータベース保存までのバックエンド機能を、Pythonで構築しました。

## 背景・目的

将来的なニュースメディア運営を検討・想定しており、その一環として、以下を自力で設計・実装しました。

- RSSフィードからの記事収集
- 重複データの排除(URL単位でのUNIQUE制約)
- cronによる定期的な自動収集
- (今後拡張予定)AIを用いた要約処理

学習の過程では、AIを活用して知識を補いながらも、提示されたコードをそのまま使うのではなく、実際に動かして検証し、エラーが出た際は原因を自分でトレースして修正する、という進め方を徹底しました。

## 技術構成

- Python 3.12
- feedparser(RSS解析)
- SQLite(開発時)/ PostgreSQL(本番想定)
- Docker / Docker Compose
- cron(定期実行)

## 処理の流れ

1. DBに接続し、テーブルがなければ作成する(URL列にUNIQUE制約)
2. 指定したRSSフィードを取得する
3. 取得した記事を、Articleクラスのインスタンスに変換する
4. 1件ずつDBへ保存する
   - 新規の記事:保存
   - 既存の記事(URL重複):スキップし、処理は継続
5. cronにより、上記1〜4を定期的に自動実行する

## 工夫した点

- URLをUNIQUE制約とすることで、DB側の仕組みとして重複を防止(アプリ側のチェック漏れに依存しない設計)
- try/exceptにより、重複エラーが発生しても全体の処理を止めずに継続する設計
- Dockerでタイムゾーンを日本時間(Asia/Tokyo)に明示的に設定し、cronの実行時刻のズレ(UTCとの9時間差)を防止
- requirements.txtでライブラリのバージョンを固定し、環境差異による動作不良を防止

## 開発中に自力で解決したバグ(参考)

| バグ | 原因 | 解決方法 |
|---|---|---|
| `AttributeError: module 'feedparser' has no attribute 'parse'` | 自作ファイル名がライブラリ名と衝突していた | `feedparser.__file__`で読み込み元を確認し、原因のファイルを削除 |
| `entry.url`でAttributeError | feedparserの正しい属性名は`link`だった(自作クラスの属性名`url`と混同) | `entry.link`に修正 |
| `UNIQUE`制約が効かない | 既存テーブルが古い構造のまま残っていた | `DROP TABLE`後に、UNIQUE制約付きで`CREATE TABLE`し直し |
| cronが指定時刻に動作しない | コンテナの時刻がUTC(日本時間と9時間ズレていた) | Dockerfileに`ENV TZ=Asia/Tokyo`を追加 |
| `python3: not found`(cron実行時) | cronは通常のシェルと異なるPATHで動作するため、コマンドの場所を見失う | `which python3`で正確なパスを確認し、crontabにフルパスで指定 |

## 今後の拡張予定

- 複数サイトのRSSに対応(URLをリスト化し、順次処理)
- 取得件数・頻度の調整(1日トータル3〜10件程度を想定)
- AIによる要約・言い換え処理の追加
- SQLiteからPostgreSQLへの移行(本番想定)