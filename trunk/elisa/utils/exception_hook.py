
import cgitb, os, sys, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Header import Header

class NullFile:

    def write(self, data):
        pass

class EmailTracebackHook(cgitb.Hook):

    email_send = False
    
    def set_mail_parameters(self, author, recipients, subject, smtp_server):
        self.mail_from = author
        self.mail_to = recipients
        self.mail_subject = subject
        self.smtp_server = smtp_server
        self.email_send = True
        
    def get_last_tb(self):
        """ Fetch the last traceback data in logdir and purge the
        directory. Thus we are sure there is only one traceback in the
        directory at a time.
        """
        files = os.listdir(self.logdir)
        assert len(files) == 1
        path = os.path.join(self.logdir, files[0])
        f = open(path)
        tb = f.read()
        os.unlink(path)
        return tb

    def handle(self, info=None):
        """ add-on to default cgitb.handle():

        - if logdir doesn't exists, create it
        - if format == mail, send traceback via mail
        """
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
            
        cgitb.Hook.handle(self, info=info)
        if self.format == 'mail':
            self.send_mail(self.get_last_tb())

    def send_mail(self, mail_data):
        if self.email_send:
            print 'Sending traceback via mail ...'
        else:
            print mail_data
            return
        
        subject = self.mail_subject
        sender = self.mail_from
        recipients = self.mail_to
        encoding = 'iso-8859-1'
        
        if not mail_data:
            return
        
        msg = MIMEMultipart("alternative")
        
        msg['Subject'] = Header(subject, encoding)
        msg['To'] = str(recipients)[1:-1].replace('\'','')
        msg['MIME-Version'] = "1.0"
        msg.epilogue = ''

        textPart = MIMEText(mail_data,encoding)
        msg.attach(textPart)

        server = smtplib.SMTP(self.smtp_server)
        try:
            server.sendmail(sender, recipients, msg.as_string())
        except smtplib.SMTPRecipientsRefused,msg:
            print 'mail was refused by smtp server'
        server.quit()
        
def set_exception_hook(mail_from, mail_to, mail_subject, smtp_server):
    " override the default exception hook with out customized one "
    print 'set exception hook'
    hook = EmailTracebackHook(file=NullFile(), display=0,
                              logdir='tracebacks', format='mail')
    hook.set_mail_parameters(mail_from, mail_to, mail_subject, smtp_server)
    sys.excepthook = hook


def test_hook(some_int):
    print "start some_int>>", some_int
    return_int = 10 / some_int
    print "end some_int>>", some_int
    return return_int

if __name__ == "__main__":
    set_exception_hook("elisa@localhost", ["phil@base-art.net",],
                       "Elisa crashed", "localhost")
    test_hook(0)
