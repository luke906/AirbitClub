import getpass, poplib, email
import base64

Mailbox = poplib.POP3_SSL('pop.naver.com')

Mailbox.user("luke906")
Mailbox.pass_('newlife8661!')
numMessages = len(Mailbox.list()[1])

## get mail box stats; returns an array
pop3_stat = Mailbox.stat()
print("Total New Mails : %s (%s bytes)" % pop3_stat)

body_contents = ""

for i in range(numMessages):
    raw_email  = b"\n".join(Mailbox.retr(i+1)[1])
    parsed_email = email.message_from_bytes(raw_email)

    if parsed_email.is_multipart():
        for part in parsed_email.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body_contents = part.get_payload(decode=True)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body_contents = parsed_email.get_payload(decode=True)




if numMessages > 0:
    print(body_contents.decode('utf-8'))
    #메일을 읽은 상태로 표시한다.
    Mailbox.dele(numMessages)


Mailbox.quit()
