import logging
# 假设您把 serverchan3 的代码放在了 push/serverchan3.py
from .serverchan3 import push_serverchan3
# 导入我们刚写的企业微信推送模块
from .wecom_app import push_wecom_app 

__available_pusher = {
    'serverchan3': push_serverchan3,
    # 注册企业微信推送器，环境变量 WECOM_CORP_ID 存在时启用
    'wecom_app': push_wecom_app 
}

def push(all_logs: list[str]):
    logging.info("开始推送结果")
    for name, func in __available_pusher.items():
        try:
            # 这里可以加个环境变量判断，如果环境变量没配，直接跳过
            # 例如：如果 push 是 wecom_app，但没有配 WECOM_CORP_ID，则跳过
            if name == 'wecom_app':
                if not os.environ.get('WECOM_CORP_ID'):
                    continue
            func(all_logs)
        except Exception as e:
            logging.error(f"[Push] {name}时出现问题", exc_info=e)
    logging.info("推送结束")
