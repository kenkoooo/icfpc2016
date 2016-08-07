from datetime import datetime

import ProblemCrawler


def run():
    hash_text = ProblemCrawler.get_latest_snapshot_hash()
    url = ProblemCrawler.BLOB_URL + hash_text
    content = ProblemCrawler.api_access(url).json()
    p = []
    for problem in content["problems"]:
        cnt = 0
        publish_time = int(datetime.now().timestamp()) - problem["publish_time"]
        publish_time /= 60 * 60
        for ranking in problem["ranking"]:
            if ranking["resemblance"] == 1.0:
                cnt += 1
        point = problem["problem_size"] / (cnt + 1)
        p.append({"point": point, "id": problem["problem_id"], "published_time": int(publish_time)})
    p = sorted(p, reverse=True, key=lambda x: x["point"])
    p = p[:100]
    for i in p:
        print(i)


if __name__ == '__main__':
    run()
