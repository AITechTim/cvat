# Copyright (C) 2023-2024 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

import numpy as np
import torch
# import onnx
# import onnxruntime as ort
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
# from samexporter.export_sam2 import SAM2ImageEncoder
import imagehash
# import hashlib
import os

class ModelHandler:
    def __init__(self):
        self.device = torch.device('cpu')
        self.current_image_hash = None
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
            if torch.cuda.get_device_properties(0).major >= 8:
                # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True

        # onnx_model = onnx.load("./sam2_hiera_l_encoder.onnx")
        # self.ort_sess = ort.InferenceSession("./sam2_hiera_l_encoder.onnx")
        if os.getenv("SAM2_MODEL") == "tiny":
            self.model_cfg = "sam2_hiera_t.yaml"
            self.sam_checkpoint = "./samexporter/original_models/sam2_hiera_tiny.pt"
        else:
            self.model_cfg = "sam2_hiera_l.yaml"
            self.sam_checkpoint = "./samexporter/original_models/sam2_hiera_large.pt"
        print(self.model_cfg)
        # sam2_model = build_sam2(self.model_cfg, self.sam_checkpoint, device=self.device)
        # self.sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
        self.predictor = SAM2ImagePredictor(build_sam2(self.model_cfg, self.sam_checkpoint, device=self.device))

    # image: PIL Image
    def handle(self, image, pos_points, neg_points):
        # pos_points, neg_points = list(pos_points), list(neg_points)
        # print("0.o")
        image_hash = imagehash.dhash(image)
        # image_hash = hashlib.md5(image).hexdigest()
        with torch.inference_mode():
                # print("0.1")

            # x = torch.from_numpy(np.array(image)).float()            
            # high_res_feats_0, high_res_feats_1, image_embed = self.sam2_encoder(x)
            # print("0.2")

            # return high_res_feats_0, high_res_feats_1, image_embed
            if image_hash != self.current_image_hash or not self.predictor._is_image_set:
                self.current_image_hash = image_hash
                self.predictor.set_image(np.array(image))
                print("Cache miss")
            else:
                print("Cache hit")
            # features = self.predictor.get_image_embedding()
            # high_res_features = self.predictor._features["high_res_feats"]
            # return features, high_res_features


            masks, scores, _ = self.predictor.predict(
                point_coords=np.array(pos_points + neg_points),
                point_labels=np.array([1]*len(pos_points) + [0]*len(neg_points)),
                multimask_output=True,
            )
            sorted_ind = np.argsort(scores)[::-1]
            best_mask = masks[sorted_ind][0]
            return best_mask
