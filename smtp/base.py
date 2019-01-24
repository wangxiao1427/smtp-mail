#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import smtplib
from smtplib import SMTPHeloError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPNotSupportedError
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

__all__ = ['MailResponse', 'AIOSMailTemplate']

class MailResponse():

    def __init__(self, succcess, msg):
        self.success = succcess
        self.msg = msg

class BaseMailTemplate(object):
    # 发件人邮箱标签
    sender_label = '默认'
    # 发件人邮箱账号
    sender_account = ''
    # 发件人邮箱密码
    sender_passwd = ''
    # 收件人邮箱账号
    receivers = []

    message = ''

    layout = ''

    def __init__(self, **options):
        
        options = options or dict()

        self.content = options.get('content')
        self.subject = options.get('subject', 'subject')

    
    def login(self):
        cfg = self.smtp_config()

        self.server = smtplib.SMTP_SSL(*cfg)
        self.server.login(self.sender_account, self.sender_passwd)

        return self
                
    def _build_msg(self):
        self.layout = re.sub(re.compile(r'{{content}}', re.S), self.content, self.layout)
        
        self.message = MIMEText(self.layout, 'html', 'utf-8')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        self.message['From'] = formataddr([self.sender_label, self.sender_account])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        self.message['To'] = self.receivers
        self.message['Subject'] = Header(self.subject, 'utf-8')
        
    def send(self):
        try:
            self._set_layout()
            # 邮件对象
            self._build_msg()
            # 发送
            self.server.sendmail(self.sender_account, self.receivers, self.message.as_string())
            return MailResponse(True, 'success')
        except SMTPHeloError as err:
            return MailResponse(False, 'The server didn\'t reply properly to the helo greeting.')
        except SMTPRecipientsRefused as err:
            return MailResponse(False, 'The server rejected ALL recipients(no mail was sent).')
        except SMTPSenderRefused as err:
            return MailResponse(False, 'The server didn\'t accept the from_addr.')
        except SMTPDataError as err:
            return MailResponse(False, 'The server replied with an unexpected error code (other than a refusal of a recipient).')
        except SMTPNotSupportedError as err:
            return MailResponse(False, 'The mail_options parameter includes \'SMTPUTF8\' but the SMTPUTF8 extension is not supported by the server.')
        except Exception as err:
            return MailResponse(False, str(err))
            
    def __del__(self):
        self.server.quit()