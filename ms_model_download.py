# usage     : python ms_model_download.py --repo_id repo_id --revision revision
# example   : python ms_model_download.py --repo_id baichuan-inc/Baichuan2-13B-Chat-4bits --revision v1.0.2
import argparse
import time
from modelscope.hub.snapshot_download import snapshot_download


def _log(_repo_id, _type, _msg):
    date1 = time.strftime('%Y-%m-%d %H:%M:%S')
    print(date1 + " " + _repo_id + " " + _type + " :" + _msg)


def _download_model(_repo_id, _revision):    
    #_cache_dir = 'caches/' + _repo_id
    _cache_dir = 'caches/'

    try:
        #example: baichuan-inc/Baichuan2-13B-Chat-4bits
        #model_dir = snapshot_download('baichuan-inc/Baichuan2-13B-Chat-4bits', cache_dir=_cache_dir, revision='v1.0.2')
        model_dir = snapshot_download(_repo_id, cache_dir=_cache_dir, revision=_revision)
        print("Model Save Path:" + model_dir)
    except Exception as e:
        error_msg = str(e)
        if ("401 Client Error" in error_msg):
            return True, error_msg
        else:
            return False, error_msg
    return True, ""

def download_model_retry(_repo_id, _revision):
    i = 0
    flag = False
    msg = ""
    while True:
        flag, msg = _download_model(_repo_id, _revision)
        if flag:
            _log(_repo_id, "success", msg)
            break
        else:
            _log(_repo_id, "fail", msg)
            if i > 1440:
                msg = "retry over one day"
                _log(_repo_id, "fail", msg)
                break
            timeout = 60
            time.sleep(timeout)
            i = i + 1
            _log(_repo_id, "retry", str(i))
    return flag, msg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_id', default=None, type=str, required=True)
    parser.add_argument('--revision', default=None, type=str, required=True)

    args = parser.parse_args()

    download_model_retry(args.repo_id, args.revision)
