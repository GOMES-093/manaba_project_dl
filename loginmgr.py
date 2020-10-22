import requests, getpass, traceback
from bs4 import BeautifulSoup
import utils

def loadSessionId():
    # 手動で書き換えられた場合など正当性のチェックがいるかも
    # regexpで
    sessid = ''
    try:
        with open('session.txt','r') as f:
            sessid = f.readline()
        if sessid == '0':
            print('ログインしていません。')
            return None
    except IOError as e:
        print(traceback.format_exception_only(type(e), e)[0].rstrip('\n'))
        print('セッションファイルが読み込めません。')
        return None
    return sessid

def saveSessionId(sessid):
    try:
        with open('session.txt','w') as f:
            f.write(sessid)
    except IOError as e:
        print(e.message)
        print('セッションファイルが書き込めません。')
        return False
    return True

def isSessionLive(out=True):
    sessid = loadSessionId()
    if sessid == None:
        print('セッションロードエラー.')
        return False
    html = requests.get("https://cit.manaba.jp/ct/home",cookies={'sessionid':sessid})
    html.raise_for_status()
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('ul',{'class':'errmsg'})==None:
        sessid = html.cookies.get('sessionid')
        if out:
            print('ログイン成功、セッションIDは以下の通りです:')
            print(sessid)
        return True
    else:
        if out:
            print('ログイン失敗、エラーメッセージは以下の通りです:')
            print(soup.find('ul',{'class':'errmsg'}).select('li')[0].text)
        return False

def makeSession():
    if isSessionLive(out=False):
        print('すでにログインされています.')
        sessid=loadSessionId()
        print('セッションID:',sessid)
        return sessid
    print("ログインページにアクセス中...")
    html = requests.get("https://cit.manaba.jp/ct/login")
    html.raise_for_status()
    soup = BeautifulSoup(html.content, "html.parser")
    sessid = html.cookies.get('sessionid')
    userid=input("ユーザIDを入力: ")
    passwd=getpass.getpass("パスワードを入力: ")
    login = "ログイン"
    manaba_form = soup.find('input',{'name':'manaba-form'}).get('value')
    session_value1=soup.find('input',{'name':'SessionValue1'}).get('value')
    session_value=soup.find('input',{'name':'SessionValue'}).get('value')
    payload = {
        'userid' : userid,
        'password' : passwd,
        'login' : login,
        'manaba-form' : manaba_form,
        'SessionValue1' : session_value1,
        'SessionValue' : session_value,
    }
    html = requests.post("https://cit.manaba.jp/ct/login",data=payload,cookies={'sessionid':sessid})
    html.raise_for_status()
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('ul',{'class':'errmsg'})==None:
        sessid = html.cookies.get('sessionid')
        print('ログイン成功、セッションIDは以下の通りです:')
        print(sessid)
        saveSessionId(sessid)
        return sessid
    else:
        print('ログイン失敗、エラーメッセージは以下の通りです:')
        print(soup.find('ul',{'class':'errmsg'}).select('li')[0].text)
        return None

def killSession():
    sessid = loadSessionId()
    html = requests.get("https://cit.manaba.jp/ct/logout",cookies={'sessionid':sessid})
    html.raise_for_status()
    saveSessionId('0')

if __name__ == "__main__":
    session_state = isSessionLive(out=False)
    while True:
        utils.printHl()
        print('現在時刻:',utils.now())
        if session_state:
            print('セッションの状態は「有効」です。セッションID=%s'%loadSessionId())
        else:
            print('セッションの状態は「無効」です。')
        print('オペレーションを選択：')
        print('1：セッションの確認')
        print('2：ログイン')
        print('3：ログアウト')
        print('0：終了')
        sel = utils.select(['1','2','3','0'],prompt='オペレーション[0-3]:')
        utils.printHl()
        if sel == '1':
            session_state = isSessionLive()
            utils.waitForReturn()
        if sel == '2':
            session_state = makeSession()
            utils.waitForReturn()
        if sel == '3':
            killSession()
            session_state = False
            print('ログアウトしました')
            utils.waitForReturn()
        if sel == '0':
            quit()
        