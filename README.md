# MongoDB-ML Dashboard

This project integrates object detection, data storage, cloud syncing, and an interactive dashboard into a unified system. It uses Streamlit for the frontend, MongoDB for object data storage, AWS S3 for image storage, and RabbitMQ for task queuing.

## Features

1. **Image Upload and Object Detection**:
   - Upload images via a user-friendly Streamlit interface.
   - Perform object detection using pre-trained models.

2. **Data Storage**:
   - Detected objects are stored in MongoDB along with metadata.

3. **Cloud Syncing**:
   - Uses RabbitMQ to queue MongoDB entries for processing.
   - Images are uploaded to AWS S3, with each entry updated to reflect its "S3 Sync" status.

4. **Real-Time Dashboard**:
   - View detected objects and counts in an interactive dashboard.
   - Filter and interact with stored data seamlessly.

## Prerequisites

- **Python**: Ensure Python 3.8 or higher is installed.
- **MongoDB**: Install and configure MongoDB for local or remote usage.
- **RabbitMQ**: Set up RabbitMQ using the provided `rmq.sh` script.
- **AWS S3**: Configure an S3 bucket for image storage.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vinayhegde-11/mongo_ml_dashboard.git
   cd mongo_ml_dashboard
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the YOLOv7 model file:
   - Download `yolov7.pt` from [this link](https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt).
   - Place the file in the project directory.

5. Configure RabbitMQ:
   ```bash
   bash rmq.sh
   ```

6. Update the `config.yml` file with the following details:
   ```yaml
   AWS_PUBLIC_KEY: "<your-aws-public-key>"
   AWS_SECRET_KEY: "<your-aws-secret-key>"
   RABBITMQ_URL: "<rabbitmq-url>"
   IMAGE_STORE_FOLDER: "<path-to-local-image-storage-folder>"
   S3_BUCKET_NAME: "<your-s3-bucket-name>"
   MODEL_FILE: "yolov7.pt"
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run merge.py
   ```

2. Interact with the portal:
   - **Upload Image**: Add images for object detection.
   - **Dashboard**: View detected objects and their counts, along with sync statuses.

## Workflow

1. **Image Upload**:
   - The uploaded image is processed for object detection.
   - Metadata is stored in MongoDB.

2. **RabbitMQ Integration**:
   - The `push_to_rabbitmq` function in `merge.py` queues the MongoDB entry ID for further processing.

3. **S3 Upload**:
   - The `s3_upload.py` script retrieves the image path and uploads it to the specified S3 bucket.
   - The "S3 Sync" status is updated in MongoDB upon successful upload.

## File Structure

- **`merge.py`**: Main application file for the Streamlit portal.
- **`config.yml`**: Configuration file for setting up variables.
- **`s3_upload.py`**: Script for uploading images to AWS S3.
- **`rmq.sh`**: Script to configure RabbitMQ.
- **`requirements.txt`**: Lists required Python packages.

## Notes

- Ensure all required configurations in `config.yml` are correctly set before running the application.
- MongoDB must be installed and running for the application to work.
- AWS credentials should have appropriate permissions for the S3 bucket.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
