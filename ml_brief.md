# ML & Edge Model Brief - Sentinel

## Goals
- On-device ANPR (plate detection + OCR) with >95% top-1 recognition for SA plates in good light.
- Gunshot detection with <2% false positive rate in urban noise.
- Violent-motion/weapon detection for 2-3 second clips with precision >85% at recall 75%.

## Model stack
- ANPR: YOLOv5-lite (detector) -> lightweight CRNN OCR (quantized, TFLite)
- Gunshot: 1D-CNN on spectrograms (MFCC) or lightweight transformer; quantized to EdgeTPU
- Violent-motion: MobileNet3 3D Conv (temporal) small model

## Edge targets
- NVIDIA Jetson Nano / Xavier NX (for heavy ops)
- Raspberry Pi 4 + Coral Edge TPU for constrained nodes
- Android mobile devices (ARM) using TFLite models

## Datasets needed (public + procurement)
- SAPS incident videos (procure via data sharing agreements)
- Synthetic dashcam footage (simulate different angles, motion blur, nighttime)
- Gunshot acoustic datasets (UrbanSound8K, others; collect controlled shots for SA ballistics)
- ANPR plate images for South African plates (collect from partner fleets; synth plate generator)

## Evaluation metrics
- Precision/Recall per event type
- ROC AUC for gunshot classifier
- mAP@0.5 for plate detection
- End-to-end latency (ms) on target edge
- Model size <8MB for Coral, <50MB for Jetson Nano deployments

## Training & CI
- Use PyTorch for training, export to ONNX -> TFLite/EdgeTPU compile
- Continuous evaluation via held-out precincts and adversarial noise injection