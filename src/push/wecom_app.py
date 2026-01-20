# push/wecom_app.py
import logging
import os
import requests
from typing import List
from datetime import date

def push_wecom_app(all_logs: List[str]):
    """
    通过企业微信应用发送消息
    需要配置环境变量:
        WECOM_CORP_ID: 企业ID
        WECOM_CORP_SECRET: 应用的Secret
        WECOM_AGENT_ID: 应用的AgentId
        WECOM_TO_USER: 接收人 (可选, 默认 @all)
    """
    corp_id = os.getenv('WECOM_CORP_ID', '').strip()
    corp_secret = os.getenv('WECOM_CORP_SECRET', '').strip()
    agent_id = os.getenv('WECOM_AGENT_ID', '').strip()

    # 如果关键配置缺失，直接返回（不报错，只是不推送）
    if not corp_id or not corp_secret or not agent_id:
        return

    # 获取 access_token
    try:
        token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}"
        resp = requests.get(token_url, timeout=10)
        result = resp.json()
        
        if result.get("errcode") != 0:
            logging.error(f"企业微信获取Token失败: {result.get('errmsg')}")
            return
        
        access_token = result["access_token"]
    except Exception as e:
        logging.error("获取企业微信Token异常", exc_info=e)
        return

    # 准备消息内容
    to_user = os.getenv('WECOM_TO_USER', '@all').strip() # 默认发给所有人
    title = f"森空岛自动签到结果 - {date.today().strftime('%Y-%m-%d')}"
    content = "\n".join(all_logs) if all_logs else "今日无可用账号或无输出"

    # 发送消息
    msg_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": int(agent_id),
        "text": {
            "content": f"【{title}】\n\n{content}"
        },
        "safe": 0
    }

    try:
        r = requests.post(msg_url, json=payload, timeout=10)
        result = r.json()
        if result.get("errcode") != 0:
            logging.error(f"企业微信推送失败: {result.get('errmsg')}")
        else:
            logging.info("企业微信推送成功")
    except Exception as e:
        logging.error("企业微信推送异常", exc_info=e)
