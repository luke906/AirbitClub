from __future__ import print_function
import lxml.etree
import lxml.html
import base64
import os
import argparse
import dateutil.parser as parser
import httplib2
from apiclient import discovery
from apiclient import errors
from bs4 import BeautifulSoup
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class Gmail_Manager:

    def __init__(self):
        try:
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

        self.service = None

    # ex: secret_json_file -> 'gmail-python-chargerunit05.json'
    def get_credentials(self, secret_json_file):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = "../Gmail_Credentials" #os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       secret_json_file)

        store = Storage(credential_path)
        credentials = store.get()

        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)

        return credentials

    def get_service(self):
        return self.service

    def ListMessagesMatchingQuery(self, user_id, query=''):
        """List all Messages of the user's mailbox matching the query.

      Args:
        _service: Authorized Gmail API _service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

      Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """
        try:
            response = self.service.users().messages().list(userId=user_id,
                                                        q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(userId=user_id, q=query,
                                                            pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def ListMessagesWithLabels(self, user_id, label_ids=[]):
        """List all Messages of the user's mailbox with label_ids applied.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.

      Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
      """
        try:
            response = self.service.users().messages().list(userId=user_id,
                                                        labelIds=label_ids).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(userId=user_id,
                                                            labelIds=label_ids,
                                                            pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def GetMessage(self, user_id, msg_id):
        """Get a Message with given ID.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

      Returns:
        A Message.
      """
        try:
            message = self.service.users().messages().get(userId=user_id, id=msg_id).execute()

            print("Message snippet: %s" % message['snippet'])

            print(message['payload']['parts']['body'])

            return message
        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def get_unread_message_count(self):
        user_id = 'me'
        label_id_one = 'INBOX'
        label_id_two = 'UNREAD'

        # Getting all the unread messages from Inbox
        # labelIds can be changed accordingly
        unread_msgs = self.service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

        count = unread_msgs['resultSizeEstimate']

        # We get a dictonary. Now reading values for the key 'messages'
        try:
            mssg_list = unread_msgs['messages']
        except:
            print("total unread message count is : %d" % count)

        return count


    def get_unread_message(self):

        user_id = 'me'
        label_id_one = 'INBOX'
        label_id_two = 'UNREAD'

        # Getting all the unread messages from Inbox
        # labelIds can be changed accordingly
        unread_msgs = self.service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

        # We get a dictonary. Now reading values for the key 'messages'
        try:
            mssg_list = unread_msgs['messages']
        except:
            print("there is no new messages")
            return

        print("Total unread messages in inbox: ", str(len(mssg_list)))

        final_list = []

        for mssg in mssg_list:
            temp_dict = {}
            m_id = mssg['id']  # get id of individual message
            message = self.service.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
            payld = message['payload']  # get payload of the message
            headr = payld['headers']  # get header of the payload

            for one in headr:  # getting the Subject
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['Subject'] = msg_subject
                else:
                    pass

            for two in headr:  # getting the date
                if two['name'] == 'Date':
                    msg_date = two['value']
                    date_parse = (parser.parse(msg_date))
                    m_date = (date_parse.date())
                    temp_dict['Date'] = str(m_date)
                else:
                    pass

            for three in headr:  # getting the Sender
                if three['name'] == 'From':
                    msg_from = three['value']
                    temp_dict['Sender'] = msg_from
                else:
                    pass

            temp_dict['Snippet'] = message['snippet']  # fetching message snippet

            try:

                # Fetching message body
                mssg_parts = payld['parts']  # fetching the message parts
                part_one = mssg_parts[0]  # fetching first element of the part
                part_body = part_one['body']  # fetching body of the message
                part_data = part_body['data']  # fetching data from the body
                clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
                clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean_two, "lxml")
                mssg_body = soup.body()

                # mssg_body is a readible form of message body
                # depending on the end user's requirements, it can be further cleaned
                # using regex, beautiful soup, or any other method
                temp_dict['Message_body'] = mssg_body

            except:
                pass

            final_list.append(temp_dict)  # This will create a dictonary item in the final list

            # This will mark the messagea as read
            self.service.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

        print("Total messaged retrived: ", str(len(final_list)))

        return final_list


