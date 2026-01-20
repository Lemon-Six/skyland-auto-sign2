import logging
import os  # 注意：原代码中使用了 os.environ，需要导入 os
from typing import List  # 修复点：导入 List 以兼容旧版 Python

# 假设您把 serverchan3 的代码放在了 push/serverchan3.py
from .serverchan3 import push_serverchan3
# 导入我们刚写的企业微信推送模块
from .wecom_app import push_wecom_app

__available_pusher = {
    'serverchan3': push_serverchan3,
    # 注册企业微信推送模块
    'wecom_app': push_wecom_app
}

# 修复点：使用 List[str] 代替 list[str]
def push(all_logs: List[str]):
    logging.info("开始推送结果")
    for name, func in __available_pusher.items():
        try:
            # 这里可以加个环境变量判断，如果环境变量没配，直接跳过
            if name == 'wecom_app':
                if not os.environ.get('WECOM_CORP_ID'):
                    continue
            func(all_logs)
        except Exception as e:
            logging.error(f"[Push] {name}时出现问题", exc_info=e)
    logging.info("推送结束")
