# SSD in TensorFlow: Traffic Sign Detection and Classification
## Overview
Implementation of [Single Shot MultiBox Detector (SSD)] in TensorFlow, to detect and classify traffic signs. This implementation was able to achieve 40-45 fps .



Currently only stop signs and pedestrian crossing signs are detected. 





## Dependencies
* Python 3.5+
* TensorFlow v0.12.0
* Pickle
* OpenCV-Python
* Matplotlib (optional)



## Differences between original SSD implementation
Obivously, we are only detecting certain traffic signs in this implementation, whereas the original SSD implemetation detected a greater number of object classes in the PASCAL VOC and MS COCO datasets. Other notable differences are:
* Uses AlexNet as the base network
* Input image resolution is 400x260
* Uses a dynamic scaling factor based on the dimensions of the feature map relative to original image dimensions

## Performance
As mentioned above, this SSD implementation was able to achieve 40-45 fps on a GTX 1080 with an Intel Core i7 6700K.

The inference time is the sum of the neural network inference time, and Non-Maximum Suppression (NMS) time. Overall, the neural network inference time is significantly less than the NMS time, with the neural network inference time generally between 7-8 ms, whereas the NMS time is between 15-16 ms. The NMS algorithm implemented here has not been optimized, and runs on CPU only, so further effort to improve performance can be done there.

## Dataset characteristics
The entire LISA Traffic Sign Dataset consists of 47 distinct traffic sign classes. Since we are only concered with a subset of those classes, we only use a subset of the LISA dataset. Also, we ignore all training samples where we do not find a matching default box, further reducing our dataset's size. Due to this process, we end up with very little data to work with.

In order to improve on this issue, we can perform image data augmentation, and/or pre-train the model on a larger dataset (e.g. VOC2012, ILSVRC)

## Training process
Given the small size of our pruned dataset, I chose a train/validation split of 95/5. The model was trained with Adadelta optimizers, with the default parameters provided by TensorFlow. The model was trained over 200 epochs, with a batch size of 32.

## Areas of improvement
There are multiple potential areas of improvement in this project:

* Pre-train the model on VOC2012 and/or ILSVRC
* Image data augmentation
* Hyper-parameter tuning
* Optimize NMS alogorithm, or leverage existing optimized NMS algorithm
* Implement and report mAP metric
* Try different base networks
* Expand to more traffic sign classes
