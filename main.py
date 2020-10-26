import requests, os, urllib.parse, zipfile
from bs4 import BeautifulSoup
import shutil
import loginmgr

### 更新履歴 ###
# 201012-2150 : zip内のファイル名がshift-jis(cp932)でも解凍できるように。
#             : shutilを利用することで、「__MACOSX」の削除を確実に。
# 201012-1003 : 複数ファイルに対応すべく、名前でフォルダを作って入れるように。
# 201015-1325 : load_urlがコード部の中にもあったのを消した。
#             : printの文に進捗表示を追加。
#             : 各個人の提出物をフォルダにまとめるかどうか変更できるように。
# 201022-1033 : 講義名とプロジェクト名を抽出し、それをフォルダ名にするように。
#        1049 : URLを実行時に入力出来るように。

### 設定項目 ###
#
# プロジェクト内の「提出物を確認」のURLをここに貼る
# 空にすると実行時に入力させる。ターミナルにコピペのが楽よね
load_url     =  ""
# 各個人の提出物をそれぞれのフォルダにまとめるか(True/False)
# 一人当たり2つ以上のファイルがある場合はTrueのがいいです
named_folder  = True
# フォルダの先頭に連番(True/False)
# 出席とかとるときは便利かも
serial_folder = True
#
###############

if load_url == "":
    print('プロジェクト内の「提出物を確認」のページのURLを入力')
    load_url = input('-->')
    if load_url == "":
        print('キャンセル')
        quit()
#セッションの読み込みorログイン
session_id = loginmgr.makeSession()
if session_id == None:
    print('ログインエラー。')
    quit()
# Webページを取得して解析する
base_url = "https://cit.manaba.jp/ct/"
cookie = {"sessionid":session_id}
html = requests.get(load_url,cookies=cookie)
soup = BeautifulSoup(html.content, "html.parser")
#講義名、プロジェクト名取得
cname=soup.find('a',{'id':'coursename'}).text
pname=soup.find('div',{'class':'peoject-header project-header-s project-headerV2'}).select('h1')[0].select('a')[0].text
dir_name=cname+'/'+pname
#フォルダがなければ作る
dir_path="./"+dir_name+"/"
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
# IDで検索し、その中のすべてのliタグを検索して表示する
chap = soup.find(class_="team-memberlist")    # idが「team-memberlist」を検索
n = len(chap.select("li"))
print("%d件のダウンロードを開始"%n)
for i,element in enumerate(chap.select("li"),start=1):    # その中のliタグの文字列を表示
    print("[%d/%d]名前：%s"%(i,n,element.text))
    name=element.text
    if serial_folder:
        name = str(i)+"_"+element.text
    name_path=dir_path+name+"/"
    if not named_folder:
        name_path = dir_path
    name = element.text+"_"
    next_url = base_url+element.select("a")[0]['href']
    print("リンク先をオープン..")
    html2 = requests.get(next_url,cookies=cookie)
    soup2 = BeautifulSoup(html2.content, "html.parser")
    if not os.path.exists(name_path):
        os.mkdir(name_path)
    s2f=soup2.find(class_="attachments attachmentsfile").select("li")
    for j,dl_linkli in enumerate(s2f,start=1):
        dl_link = dl_linkli.select("a")[0]["href"]
        print("ファイルを受信中..(%d/%d)"%(j,len(s2f)))
        fget = requests.get(base_url+dl_link,cookies=cookie)
        fname = urllib.parse.unquote(dl_link.split("/")[-1])
        print("ファイルを書き込み中..")
        with open(name_path+name+fname,"wb") as f:
            f.write(fget.content)
        if fname.endswith('.zip'):
            try:
                with zipfile.ZipFile(name_path+name+fname) as existing_zip:
                    for k,info in enumerate(existing_zip.infolist(),start=1):
                        info.filename = name+info.filename.encode('cp437').decode('utf-8')
                        print("圧縮ファイルを解凍中..%d/%d"%(k,len(existing_zip.infolist())))
                        existing_zip.extract(info, path=name_path)
                print("圧縮ファイルを削除")
                os.remove(name_path+name+fname)
                if os.path.exists(name_path+name+"__MACOSX"):
                    shutil.rmtree(name_path+name+"__MACOSX")
            except UnicodeDecodeError:
                try:
                    print("ファイル名のデコードに失敗,cp932を試します")
                    with zipfile.ZipFile(name_path+name+fname) as existing_zip:
                        for k,info in enumerate(existing_zip.infolist(),start=1):
                            info.filename = name+info.filename.encode('cp437').decode('cp932')
                            print("圧縮ファイルを解凍中..%d/%d"%(k,len(existing_zip.infolist())))
                            existing_zip.extract(info, path=name_path)
                    print("圧縮ファイルを削除")
                    os.remove(name_path+name+fname)
                    if os.path.exists(name_path+name+"__MACOSX"):
                        shutil.rmtree(name_path+name+"__MACOSX")
                except UnicodeDecodeError:
                    print("解凍できませんでした")
                finally:
                    pass
            finally:
                pass
        if os.path.exists(name_path+"__MACOSX"):
            shutil.rmtree(name_path+"__MACOSX")
