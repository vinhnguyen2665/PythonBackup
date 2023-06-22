import os

from dotenv import load_dotenv
from slack_sdk import WebClient, WebhookClient
from slack_sdk.errors import SlackApiError

from beans.result_object import ResultObject
from entity.backup_info import BackupInfo
import json


class SlackUtils:
    load_dotenv()
    # client = WebClient(token=os.getenv('SLACK_TOKEN'))
    webhook = WebhookClient(os.getenv('SLACK_WEBHOOK'))

    @staticmethod
    def post_message(db_info: BackupInfo, result, color):
        try:
            #             BACKUP-PC 2023/04/22 02:00:58 AM GMT +7
            # Backup successfully 37_RFID
            # C:\DatabaseBackup\37_RFID\2023_04_22\37_RFID_Backup_2023_04_22_02_00_52.zip
            # Commit finished
            # @VinhNQ
            mentions = []
            mentions_block = []
            # message_blocks = [{
            #     "type": "section",
            #     "text": {
            #         "type": "mrkdwn",
            #         "text": "*" + db_info.host + ":" + str(db_info.port) + "/" + db_info.database_name + "*"
            #     }
            # }]
            # message_blocks = []
            msg_text = ''
            url = ''
            for text in result:
                t_var = text.split(':')[0]
                v_var = text[len(t_var) + 1:].strip()
                if str(t_var).__eq__('svn_url'):
                    # t = "<" + v_var + ">"
                    # t = "<" + db_info.svn_url + "| Repo>"
                    url = v_var
                else:
                    msg_text += text + '\n'
                # obj = {
                #     "type": "section",
                #     "text": {
                #         "type": "mrkdwn",
                #         "text": t
                #     },
                # }
                # obj = {
                #     "title": t,
                #     "value": t,
                #     "short": False
                # },
                # message_blocks.append(obj)
            mention = ''
            if db_info.mentions:
                mentions = json.loads(db_info.mentions)
                for men in mentions:
                    # mention += men + " "
                    msg_text += men + " "
                # message_blocks += mentions_block
            # fields = [
            #     {
            #         "title": "A field's title",
            #         "value": "This field's value",
            #         "short": False
            #     },
            #     {
            #         "title": "A short field's title",
            #         "value": "A short field's value",
            #         "short": True
            #     },
            #     {
            #         "title": "A second short field's title",
            #         "value": "A second short field's value",
            #         "short": True
            #     }
            # ]
            if db_info.database_name:
                context = "/" + db_info.database_name + " <" + url + "| Download>"
            else:
                context = " " + db_info.remote_folder
            message_attachments = [
                {
                    "mrkdwn_in": ["text"],
                    "color": color,
                    # "pretext": "Optional pre-text that appears above the attachment block",
                    # "author_name": "author_name",
                    # "author_link": "http://flickr.com/bobby/",
                    # "author_icon": "https://placeimg.com/16/16/people",
                    # "title": "*" + db_info.host + ":" + str(db_info.port) + "/" + db_info.database_name + "*",


                    "title": db_info.host + ":" + str(
                        db_info.port) + context,
                    # "title_link": url,
                    "text": msg_text,
                    # "fields": fields,
                    # "thumb_url": "http://placekitten.com/g/200/200",
                    # "footer": "footer",
                    # "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                    # "ts": 123456789
                }
            ]
            # response = SlackUtils.client.chat_postMessage(
            #     channel=os.getenv('SLACK_CHANNEL'),
            #     # text=db_info.database_name,
            #     color="#1666EE",
            #     # blocks=mentions_block,
            #     attachments=message_attachments)
            response = SlackUtils.webhook.send(
                attachments=message_attachments)
            print(response.body)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
