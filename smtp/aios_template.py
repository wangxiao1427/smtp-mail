#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from smtp.base import BaseMailTemplate


class AIOSMailTemplate(BaseMailTemplate):
    """
    字典参数 :  
    `subject` : 邮件主题  
    `content` : 邮件内容  
    `receivers` : 邮件接收者列表, ['xxx@qq.com','yyy@qq.com'] 或 'xxx@qq.com,yyy@qq.com'  
    """
    sender_label = 'AIOS'
    # 发件人邮箱账号
    sender_account = ''
    # 发件人邮箱密码
    sender_passwd = ''

    def __init__(self, **options):
        """
        字典参数 :  
        `subject` : 邮件主题  
        `content` : 邮件内容  
        `receivers` : 邮件接收者列表, ['xxx@qq.com','yyy@qq.com'] 或 'xxx@qq.com,yyy@qq.com'  
        """

        options = options or dict()

        _sender_account = options.pop('sender_account')
        _sender_passwd = options.pop('sender_passwd')

        if not _sender_account or not _sender_passwd:
            raise Exception('\'sender_account\' or \'sender_passwd\' is missing or invalidate')

        self.sender_account = _sender_account
        self.sender_passwd = _sender_passwd

        _receivers = options.pop('receivers')
        if _receivers:
            if isinstance(_receivers, list):
                self.receivers = ','.join(_receivers)
            else:
                self.receivers = str(_receivers)
        
        super().__init__(**options)
        
    
    def smtp_config(self):
        # (host, port)
        return ('smtp.exmail.qq.com', 465)

    def _set_layout(self, kind='default'):
        if kind == 'default':
            template_file = os.path.join(os.getcwd(), 'templates', 'Christmas Special Offer.html')
            if not os.path.exists(template_file):
                raise Exception('文件找不到!')
            with open(template_file, 'r') as f:
                self.layout = f.read()
