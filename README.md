# manabaのプロジェクトに提出されたレポート一括ダウンローダー
### 概要
PythonのWebスクレイピングでmanabaのプロジェクトに提出された提出物を一括でダウンロードする
### 開発動機
プロジェクト上の提出物をすべて確認するために、すべての受講者のリンクを一人ずつクリックして、その中の提出ファイルのリンクをクリックして…という作業が面倒だったから。
### 使い方
あらかじめmanabaでプロジェクト内の「提出物を確認」のページを開いて、そのURLをコピーしておく  
こんな感じのURL→```https://xxx.manaba.jp/ct/course_xxxxxx_psubmission_xxxxxx```  
main.pyを実行(Python3)  
URLを問われるので、コピーしておいたURLを貼り付ける  
manabaのIDとパスワードを入力してログイン（セッションidがカレントディレクトリ内のsession.txtに保存されるので、次に使うときセッションがタイムアウトするまではログイン情報を入れる必要がありません）  
あとは勝手にダウンロードされます。zipファイルも勝手に解凍します。  
