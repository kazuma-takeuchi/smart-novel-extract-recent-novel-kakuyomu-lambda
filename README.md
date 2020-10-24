# smart-novel-extract-recent-novel-kakuyomu-lambda
カクヨムのサイトからスクレイピング対象の小説のみ抽出する

## 設定  
| 項目 | 値 |
| ---- | ---- |
| ランタイム | Python 3.8 |
| メモリ | 512 MB |
| タイムアウト | 5 s |
| layer | scrape_layer |

## 環境変数  
| 変数名 | 値 |
| ---- | ---- |
| PKEY | scraping-target |
| SKEY | kakuyomu |
| TABLE_NAME | control |