# discord-bot-macha
must have an alpha channel

## overview
Discordのテキストチャンネルに貼られた画像が, Xに透過した際に正しく透過画像のままになるかvalidationする

### 検証条件
- 添付ファイルがpngであるなら
  - サイズが900px * 900px以下
  - アルファチャンネルが100でない箇所が存在する
- まとめてアップされた画像のうち, 1枚以上が上記の条件を満たすこと