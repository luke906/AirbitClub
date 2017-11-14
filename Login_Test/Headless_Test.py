import getpass, poplib, email

Mailbox = poplib.POP3('pop.naver.com')

Mailbox.user("luke906")
Mailbox.pass_('newlife8661!')
numMessages = len(Mailbox.list()[1])
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
        body_contents = b.get_payload(decode=True)


print(body_contents)