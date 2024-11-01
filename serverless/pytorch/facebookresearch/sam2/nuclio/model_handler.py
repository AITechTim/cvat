# Copyright (C) 2023-2024 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

import numpy as np
import torch
import onnx
import onnxruntime as ort
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from samexporter.export_sam2 import SAM2ImageEncoder

class ModelHandler:
    def __init__(self):
        self.device = torch.device('cpu')
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
            if torch.cuda.get_device_properties(0).major >= 8:
                # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True

        # onnx_model = onnx.load("./sam2_hiera_l_encoder.onnx")
        # self.ort_sess = ort.InferenceSession("./sam2_hiera_l_encoder.onnx")
        
        sam2_model = build_sam2(self.model_cfg, self.sam_checkpoint, device=self.device)
        self.sam2_encoder = SAM2ImageEncoder(sam2_model).cpu()
        # self.sam_checkpoint = "./sam2_hiera_large.pt"
        # self.model_cfg = "sam2_hiera_l.yaml"
        # self.predictor = SAM2ImagePredictor(build_sam2(self.model_cfg, self.sam_checkpoint, device=self.device))

    def handle(self, image, pos_points, neg_points):
        # pos_points, neg_points = list(pos_points), list(neg_points)
        with torch.inference_mode():
            high_res_feats_0, high_res_feats_1, image_embed = self.sam2_encoder(img)

            return high_res_feats_0, high_res_feats_1, image_embed

            # self.predictor.set_image(np.array(image))
            # features = self.predictor.get_image_embedding()
            # high_res_features = self.predictor._features["high_res_feats"]
            # return features, high_res_features


            # masks, scores, _ = self.predictor.predict(
            #     point_coords=np.array(pos_points + neg_points),
            #     point_labels=np.array([1]*len(pos_points) + [0]*len(neg_points)),
            #     multimask_output=True,
            # )
            # sorted_ind = np.argsort(scores)[::-1]
            # best_mask = masks[sorted_ind][0]
            # return best_mask
