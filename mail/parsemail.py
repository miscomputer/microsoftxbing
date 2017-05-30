# -*- coding: utf-8 -*-
from email.header import decode_header
from email.utils import parseaddr
from popmail import *
from basefunc.strdecoding import Decode4Str
import chardet

class ParseEmail:
    """
    解析邮件
    """

    def __init__(self,msg):
        self.msg = msg
        self.sender = ''
        self.to = ''
        self.subject = ''

    def decode_str(self,s):
        """
        获取编码
        :param s:
        :return:
        """
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def mailstruc(self):
        sender = ''
        subjects = ''
        to = ''
        for header in ['From','Subject','To']:
            value = self.msg.get(header, '')
            # print value
            if value:
                if header == 'Subject':
                    value = self.decode_str(value)
                    subjects = ''.join(value)
                    # print subjects
                elif header == 'From':
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
                    sender = value
                    # print sender
                elif header == 'To':
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
                    to = value
                    # print to
        return subjects, sender, to


if __name__ == '__main__':
    st = MailConn(host='pop.exmail.qq.com',user='xb04@datatang.cn',pw='Zaixian2015',port=995)
    count = st.userauth()
    print '总邮件数:{}'.format(count[0])
    msg = st.mailmsg(serial=(463,464))
    mail = ParseEmail(msg)
    ret = mail.mailstruc()
    print ret[1]
    filelog = open('mailtest.log','w+')

    print isinstance(ret[0], unicode)
    filelog.write(ret[0]+'\r')
    filelog.write(''.join(ret[1]+'\r'))
    filelog.write(ret[2])
    # print unicode(ret[0],'utf-8')
    filelog.flush()
    filelog.close()

