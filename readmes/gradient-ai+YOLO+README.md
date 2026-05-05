# YOLOv8 Web UI

[![Gradient](https://assets.paperspace.io/img/gradient-badge.svg)](https://console.paperspace.com/github/gradient-ai/yolo/blob/master/YOLO.ipynb?machine=Free-GPU)

This Gradio application is designed to facilitate the end-to-end creation of a YOLOv8 object detection model.

## Capabilities

- **Label Images**: this tab lets you upload images, either in bulk or one at a time, to be labeled. The bounding boxes are automatically detected, and the labels are assigned through a textbox. Entries are separated by semi-colons
- **Image Gallery**: this tab allows us to view our labeled images, seperated by the assigned training split
- **Train**: train any of the YOLOv8 models on the labeled images. Outputs the validation metrics and the best trained model from the run, `best.pt`
- **Inference**: predict object labels on images and videos. Works for direct upload and URL submission

## Next steps

- Implement streaming video support for live object detection
- Integrate with RoboFlow for easy uploading of prelabeled datasets

## Thanks and credits to:

- This application wouldn't have been feasible without the groundwork completed by the researchers for the [GLIGEN](https://github.com/gligen/GLIGEN) project. Their bounding box detector code was instrumental to making this work.
- [Ultralytics](https://github.com/ultralytics/ultralytics) for their incredible work on YOLOv8
