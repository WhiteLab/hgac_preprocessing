import smtplib
import socket

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DEFAULT_REPLY_TO = 'chiyipho@uchicago.edu'

html_style = '''
<STYLE>
h1 {font-size:'12px';}
h2 {font-size:'11px';}
th {
    font-family:courier;
    font-size:12px;
    background-color:#7D0000;
    color:white;
}
td {
    font-family:courier;
    font-size:10px;
    white-space:nowrap;
    text-align:right;
}
</STYLE>
'''


def send_mail(api_key=None, to=None, cc=None, reply_to=None, subject=None,
              content=None, html_files=None):
    # Set up from address and SMTP server
    from_address = 'mailer@{}'.format(socket.gethostname())
    server = smtplib.SMTP('localhost')

    # Ensure to is provided as either a string or a list
    if to is not None:
        if type(to) == str:
            to = [to]
    else:
        raise Exception('To address not provided')

    # Ensure cc is provided as either a string or a list
    if cc is not None:
        if type(cc) == str:
            cc = [cc]
    else:
        cc = []

    # Ensure subject is provided as a string
    if type(subject) != str:
        try:
            subject = str(subject)
        except:
            subject = ''

    # Ensure reply-to field is given, otherwise set to default
    if type(reply_to) != str:
        reply_to = DEFAULT_REPLY_TO

    # Construct email headers
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = ', '.join(to)
    msg['Cc'] = ', '.join(cc)
    msg['Reply-To'] = reply_to

    # Ensure html_files is given as a list
    if html_files is None:
        html_files = []

    # Build html content
    html_content = ''
    for html_filepath in html_files:
        print 'emailing demultiplex summary file: {}'.format(html_filepath)
        with open(html_filepath) as html_file:
            html_content += html_file.read()

    # Combine all content
    content = '<br/>\n'.join([content.replace('\n', '<br/>\n'), html_style, html_content])

    # Both content parts will have the same content.
    # If HTML is enabled, it will display as html, otherwise it will display
    # as text with HTML tags interspersed. This will be ugly, but likely won't
    # ever happen.
    text_part = MIMEText(content, 'plain')
    html_part = MIMEText(content, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    server.sendmail(from_address, to, msg.as_string())
    server.quit()


# def send_mail(api_key=None, to=None, cc=None, reply_to=None, subject=None,
#               content=None, html_files=None):
#     """
#
#     :param api_key:
#     :param to: list of email address strings
#     :param cc: list of email address strings
#     :param reply_to: email address string
#     :param content: string
#     :param html_files: list of files containing html
#     :param subject:
#     :return:
#     """
#     print "Emailer sending this in content: {}".format(content)
#     mandrill_client = mandrill.Mandrill(api_key)
#     message = {
#         "to": [],
#         "global_merge_vars": [],
#         "subject": subject,
#     }
#     if to:
#         for address in to:
#             message['to'].append({"email": address, "type": "to"})
#
#     if cc:
#         for address in cc:
#             message['to'].append({"email": address, "type": "cc"})
#
#     if reply_to:
#         message['from_email'] = reply_to
#         #message['text'] = content
#
#     html_content = ''
#     if html_files:
#         for filename in html_files:
#             print "emailing demultiplex summary file: {}".format(filename)
#             with open(filename, 'r') as f:
#                 html_content += f.read()
#
#     content = content.replace('\n', '<br>\n')
#
#     message['html'] = '<br>\n'.join([content, html_content, html_style])
#
#     result = mandrill_client.messages.send(message=message, async=False,
#                                            ip_pool='Main Pool')
#     print "Sent email via mandrill:\n{}".format(result)
