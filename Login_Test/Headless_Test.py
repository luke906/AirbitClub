import getpass, poplib, email

Mailbox = poplib.POP3('pop.naver.com')

Mailbox.user("luke906")
Mailbox.pass_('newlife8661!')
numMessages = len(Mailbox.list()[1])

for i in range(numMessages):
    raw_email  = b"\n".join(Mailbox.retr(i+1)[1])
    parsed_email = email.message_from_bytes(raw_email)
    if parsed_email.is_multipart():
        for payload in parsed_email.get_payload():
            # if payload.is_multipart(): ...
            print(payload.get_payload())
    else:
        print(parsed_email.get_payload())
    #print(parsed_email)
