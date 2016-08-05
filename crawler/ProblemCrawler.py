import argparse
import os
import time

import requests

API_KEY = "22-000a29544e7a05f9e6cb21a0b827da82"
API_URL = "http://2016sv.icfpcontest.org/api/"
BLOB_URL = API_URL + "blob/"
LIST_URL = API_URL + "snapshot/list"
HEADERS = {
    "X-API-Key": API_KEY
}


def api_access(url):
    """
    API を叩いて、ついでに1秒まつ
    毎回 1 秒待つのがアホらしいので作った。
    :param url: API の URL
    :return: 結果
    """
    content = requests.get(url, headers=HEADERS)
    time.sleep(1)
    return content


def input_file_name(problem_id):
    """
    問題 id からファイル名を作る。割とどうでもいい。
    :param problem_id: 問題 id
    :return: ファイル名
    """
    return "problem_{problem_id}.txt".format(problem_id=problem_id)


def get_latest_snapshot_hash():
    """
    最新のスナップショットのハッシュを取得します。
    :return: ハッシュ取得文字列
    """
    snapshots = api_access(LIST_URL).json()
    snapshots = sorted(snapshots["snapshots"], key=lambda x: x["snapshot_time"], reverse=True)
    return snapshots[0]["snapshot_hash"]


def get_problem_content(problem_spec_hash):
    """
    入力ファイルの内容をお届け！
    :param problem_spec_hash:
    :return:
    """
    hash_url = BLOB_URL + problem_spec_hash
    return api_access(hash_url).text


def run(args):
    """
    最新のスナップショットから問題一覧を引っ張ってきて、ディレクトリに同期する
    :param args: パース済みの引数
    :return:
    """
    print("Loading snapshot...")
    snapshot_hash = get_latest_snapshot_hash()

    # 問題一覧を取ってくる
    print("Loading problem list...")
    hash_url = BLOB_URL + snapshot_hash
    problems = api_access(hash_url).json()["problems"]
    problems = [{
                    "problem_id": p["problem_id"],
                    "problem_spec_hash": p["problem_spec_hash"]
                } for p in problems]
    print("There are " + str(len(problems)) + " problems.")

    # 保存先のディレクトリが存在しなければ作成
    path = args.d
    if not os.path.exists(path):
        os.mkdir(path)
    exist_files = os.listdir(path)

    for problem in problems:
        problem_id = problem["problem_id"]
        file_name = input_file_name(problem_id)

        if file_name in exist_files:
            # 既にファイルが存在する場合はスルー
            print(file_name + " already exists.")
        else:
            print("Downloading " + file_name + "...")
            content = get_problem_content(problem["problem_spec_hash"])
            f = open(path + "/" + file_name, "w", encoding="UTF-8")
            f.write(content)
            f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", default="./problems/", help="出力先のディレクトリを指定してね")
    run(parser.parse_args())
