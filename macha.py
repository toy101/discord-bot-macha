import io

import requests
from discord import Message, Attachment
from PIL import Image
import numpy as np

CONTENT_TYPE = 'image/png'
HEIGHT_SIZE = 900
WIDTH_SIZE = 900


class Macha:
    def __init__(self, logger):
        self.logger = logger
        self.target_channel_id = 1189234411913351168
        self.content_type = CONTENT_TYPE
        self.limit_height = HEIGHT_SIZE
        self.limit_width = WIDTH_SIZE

    def is_target_channel(self, ctx: Message) -> bool:
        if ctx.channel.id == self.target_channel_id:
            return True
        else:
            return False

    def exist_png_image(self, ctx: Message) -> bool:
        exit_png = False
        if len(ctx.attachments) >= 1:
            for attachment in ctx.attachments:
                if attachment.content_type == self.content_type:
                    exit_png = True
                    break
        return exit_png

    def valid_images(self, ctx: Message):
        valid_msg_buffer = {}
        for attachment in ctx.attachments:
            valid_messages = self._valid(attachment)
            if len(valid_messages) >= 1:
                valid_msg_buffer[attachment.filename] = valid_messages
            else:
                # 1つで透過になりうる画像があればNoneを返す
                return None

        return valid_msg_buffer

    def _valid(self, attachment: Attachment):

        valid_msg_buffer = []

        if attachment.content_type != CONTENT_TYPE:
            return valid_msg_buffer

        # sizeの確認
        if attachment.height > self.limit_height or attachment.width > self.limit_width:
            self.logger.info(
                f"{attachment.filename}'s size more big: {attachment.height}px x {attachment.width}px > {self.limit_height}px x {self.limit_width}px"
            )
            valid_msg = f"サイズが少し大きいようです: {attachment.height}px x {attachment.width}px > {self.limit_height}px x {self.limit_width}px"
            valid_msg_buffer.append(valid_msg)

        url = attachment.url.split('?')[0]
        # urlから画像を取得
        res = requests.get(url)
        img = Image.open(io.BytesIO(res.content))

        # アルファchannelが100未満のpixelが存在するか
        img_array = np.array(img)
        alpha_channel = img_array[:, :, 3] / 255
        if np.all(alpha_channel >= 1):
            self.logger.info(f"{attachment.filename} has not transparent pixel.")
            valid_msg = "透明(半透明)のピクセルが見つかりませんでした"
            valid_msg_buffer.append(valid_msg)

        return valid_msg_buffer
