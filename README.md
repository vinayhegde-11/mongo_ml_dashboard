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

5. (New) Start MongoDB using Docker:
   ```bash
   docker pull mongodb/mongodb-community-server:latest
   docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
   ```
   This will start MongoDB in a container and expose it on port 27017. The app will connect using `mongodb://localhost:27017/`.

6. Configure RabbitMQ:
   ```bash
   bash rmq.sh <username> <password>
   ```

7. Update the `config.yml` file with the following details:
   ```yaml
   aws_access_key_id: "<your-aws-access-key-id>"
   aws_secret_access_key: "<your-aws-secret-access-key>"
   s3_bucket_name: "<your-s3-bucket-name>"
   mongodb_url: "mongodb://localhost:27017/"
   rmq_user: "<rabbitmq-username>"
   rmq_pass: "<rabbitmq-password>"
   rmq_host: "localhost"
   rmq_vhost: "entries"
   rmq_topic: "<TOPIC_NAME>"
   image_dir: "<IMAGE_SAVE_PATH>"
   model_path: "yolov7.pt"
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
- MongoDB must be running (now recommended via Docker container).
- AWS credentials should have appropriate permissions for the S3 bucket.

## What's New

- **MongoDB now runs in a Docker container**: No need for local installation. The app connects to the container via `localhost:27017`.
- **Configuration improvements**: All connection URIs and credentials are now loaded from `config.yml`.
- **Code refactoring**: MongoDB, RabbitMQ, and S3 integrations are modular and configurable.
- **Bug fixes and stability**: Improved error handling and reliability for cloud sync and dashboard features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
