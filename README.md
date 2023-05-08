# FlaskBookapi
### To run the FlaskBookapi:

1. Install the required dependencies by running the following command in your terminal or command prompt: 
```pip install -r requirements.txt```

2. Place the model files "yolov3_custom_last.weights" and "yolov3_custom" in the "api" directory. 
These files contain the trained weights and configuration of a custom YOLOv3 object detection model used by the API.

3. Navigate to the api directory:
```cd api```

4. Start the Flask development server by running the following command:
```flask run```

5. Open your web browser and navigate to http://localhost:5000/ to access the FlaskBookapi.

That's it! You should now be able to upload images with titles and process them with the FlaskBookapi.
