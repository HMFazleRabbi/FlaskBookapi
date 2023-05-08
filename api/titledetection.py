import numpy as np
from classnames import classes
import cv2
import os

def load_image(image_path, scale_factor=0.4):
    """Loads an image from the specified path and resizes it by the given scale factor"""
    img = cv2.imread(image_path)
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)
    return img

def load_model(weights_path, config_path):
    """Loads a YOLOv3 model from the specified weights and configuration files"""
    net = cv2.dnn.readNet(weights_path, config_path)
    layer_names= net.getLayerNames()
    output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
    return net, output_layers

def RunInference(img, net, output_layers, confidence_threshold=0.3, nms_threshold=0.5, save_image=False):
    """Runs inference on the input image using the specified YOLOv3 model and output layers.

    Args:
        img: The input image.
        net: The YOLOv3 model.
        output_layers: The names of the output layers in the model.
        confidence_threshold: The minimum confidence score required for a detection to be considered.
        nms_threshold: The overlap threshold for non-maximum suppression.
        save_image: A flag indicating whether or not to save the output image and titles.

    Returns:
        A tuple containing the output image with bounding boxes and labels drawn around detected objects,
        and a list of the titles of the detected objects.
    """
    height, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (608, 608), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    title_list = []
    class_ids = []
    boxes = []
    confidences = []
    colors = np.random.uniform(0,255, size=(len(classes),3))
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # print( str(classes[class_id]))
            if confidence > confidence_threshold:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                print(f"class_id: {class_id}")
    
    if not class_ids:
        print("No titles detected")
        print(f"No objects detected above the confidence threshold of {confidence_threshold} and non-maximum suppression threshold of {nms_threshold}.")
        return img, []        
        # Testing code
        # return img, ["The Spirit of 'C' An Introduction to Modern Programming", 'C++ for VB Pto', 'A Book On']        

    # Perform non-maximum suppression to remove overlapping bounding boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

    # Draw bounding boxes and labels around detected objects
    font = cv2.FONT_HERSHEY_PLAIN
    output_image = img.copy()
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(output_image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(output_image, label, (x, y + 30), font, 3, color, 3)
            title_list.append(label)

    if save_image:
        # Save output image
        output_dir = 'results'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, 'output_image.jpg')
        cv2.imwrite(output_path, output_image)

        # Save output titles
        output_title_path = os.path.join(output_dir, 'output_titles.txt')
        with open(output_title_path, 'w') as f:
            for title in title_list:
                f.write(title + '/n')

        # Save output boxes
        output_box_path = os.path.join(output_dir, 'output_boxes.txt')
        with open(output_box_path, 'w') as f:
            for box in boxes:
                f.write(','.join([str(coord) for coord in box]) + '/n')

    return output_image, title_list


if __name__ == '__main__':

    weights_path = "yolov3_custom_last.weights"
    config_path = "yolov3_custom.cfg"
    net, output_layers = load_model(weights_path, config_path)


    image_path = "C:/Users/frabb/OneDrive/Desktop/WS/bookapi/api/images/1.jpg"
    img = load_image(image_path, 0.4)
    output_image, title_list = RunInference(img, net, output_layers, confidence_threshold=0.3, nms_threshold=0.5, save_image=True)

