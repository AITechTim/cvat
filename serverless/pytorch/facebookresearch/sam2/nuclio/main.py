# Copyright (C) 2023-2024 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

import json
import base64
from PIL import Image
import io
from model_handler import ModelHandler
import numpy as np
def init_context(context):
    model = ModelHandler()
    context.user_data.model = model
    context.logger.info("Init context...100%")

def handler(context, event):
    try:
        # print("0.1")
        context.logger.info("call handler")
        data = event.body
        buf = io.BytesIO(base64.b64decode(data["image"]))
        image = Image.open(buf)
        image = image.convert("RGB")  # to make sure image comes in RGB
        pos_points = data["pos_points"]
        neg_points = data["neg_points"]
        # print("0.2")
        mask = context.user_data.model.handle(image, pos_points, neg_points)
        # features, high_res_features = context.user_data.model.handle(image, pos_points, neg_points)
        # high_res_feats_0, high_res_feats_1, image_embed = context.user_data.model.handle(image, pos_points, neg_points)
        # print(len(high_res_feats_0))
        # print(high_res_feats_0[0].shape)
        # high_res_features = high_res_features[0]
        # print(image_embed)
        # print(high_res_feats_0)
        # print(high_res_feats_1)
        # image_embed = np.ascontiguousarray((features.cpu().numpy() if features.is_cuda else features.numpy()))
        # high_res_feats_0 = np.ascontiguousarray((high_res_features[0].cpu().numpy() if high_res_features[0].is_cuda else high_res_features[0].numpy()))
        # high_res_feats_1 = np.ascontiguousarray((high_res_features[1].cpu().numpy() if high_res_features[1].is_cuda else high_res_features[1].numpy()))
        # print(high_res_feats_0.shape)
        # print(high_res_feats_1.shape)
        # print(image_embed.shape)

        # return context.Response(
            # body=json.dumps({
            # 'image_embed': base64.b64encode(image_embed).decode(),
            # 'high_res_feats_0': base64.b64encode(high_res_feats_0).decode(),
            # 'high_res_feats_1': base64.b64encode(high_res_feats_1).decode(),
        # }),
        return context.Response(
            body=json.dumps({'mask': mask.tolist()}),
            headers={},
            content_type='application/json',
            status_code=200
        )
    except Exception as e:
        context.logger.error(f"Error in handler: {str(e)}")
        return context.Response(
            body=json.dumps({'error': str(e)}),
            headers={},
            content_type='application/json',
            status_code=500
        )
