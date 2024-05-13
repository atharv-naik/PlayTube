# PlayTube: A Video-on-Demand Platform built in Django

![PlayTube](/play/static/play/images/v2/PlayTube-icon-full.png)

This project is a Video-on-Demand (VOD) software service developed using Django, providing features similar to those found on YouTube. It allows users to upload videos, which are then transcoded and streamed using HLS (HTTP Live Streaming) with Adaptive Bitrate Streaming (ABS). The project also includes user authentication, social logins, video playback tracking, and more.

## Table of Contents

- [Features](#features)
- [Tools & Technologies Used](#tools--technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

1. **Video Upload, Transcoding, and Streaming:**
   - Users can upload videos which are automatically transcoded into HLS format for efficient streaming.
   - Transcoding tasks are handled asynchronously using Celery workers and a Redis queue.
   - Transcoded videos are stored on Amazon S3 for optimized content delivery.

2. **User Authentication and Social Logins:**
   - User registration, login, and logout functionalities are implemented.
   - Google social login is integrated using `django-allauth` for a seamless experience. (dev)

3. **Video Playback Tracking and Resume:**
   - User engagement is tracked by recording watch history.
   - Users can resume watching videos from where they left off.

4. **Custom HTML Email Templates:**
   - Custom email templates are implemented to notify video uploaders about successful uploads.

## Tools & Technologies Used

- Django
- Django REST Framework
- Celery
- Redis
- Amazon S3
- Ffmpeg
- `django-allauth` (for social logins)

## Installation

1. Clone the repository and navigate to the project directory.

2. Create a virtual environment and activate it:

   ```bash
    virtualenv env

    source env/bin/activate
    ```

3. Install dependencies:

   ```bash
    pip install -r requirements.txt
    ```

4. Install Ffmpeg, Redis, and Celery:

   ```bash
    sudo apt install ffmpeg redis-server celery
    ```

5. Create a .env file in the root directory and add the following environment variables to it. Replace the values with your own credentials and settings. Here's an example of the .env file content:

   ```bash
      SECRET_KEY='django-insecure-+ouf2xazl$-#nk!qjzh05k=%m68%jcmu-5z_+7m5^u70@+)v9@'
      DEBUG=0
      USE_HTTPS=0
      IP_ADDRESS='127.0.0.1:8000'
      ALLOWED_HOSTS='localhost,127.0.0.1'
      CORS_ALLOW_ALL_ORIGINS=1
      CORS_ALLOWED_ORIGINS='http:127.0.0.1:8000,yoursite1.com,yoursite2.com'
    ```

   Optional settings:

   ```bash
      DOMAIN_NAME='yoursite.com'
      CSRF_TRUSTED_ORIGINS='yoursite1.com,yoursite2.com'
      EMAIL_HOST_PASSWORD='your_gamil_app_password'
      EMAIL_HOST_USER='your_email_id'
      ADMIN_EMAIL='some_other_email_id'
   ```

6. Create a log folder for error logs in the root directory:

   ```bash
      mkdir logs
   ```

7. Make migrations and migrate:

   ```bash
      python manage.py makemigrations

      python manage.py migrate
    ```

8. Create a superuser:

   ```bash
      python manage.py createsuperuser
   ```

9. Run collectstatic before starting the server:

   ```bash
      python manage.py collectstatic
   ```

10. Run the below commands in *seperate shell environments* to start the Celery worker, the Redis server and the Django development server:

   ```bash
      python manage.py runserver
   
      redis-server
   
      celery -A playtube worker -l info
   ```

   Make sure to activate the virtual environment before running the celery worker instance.
   Navigate to `http://127.0.0.1:8000/` in your browser or to the IP:PORT you specified in the .env file (step 5)

## Usage

1. Register a new user account or login using an existing one.
2. Upload a video using the upload form.
3. Once the video is uploaded, it will be transcoded and streamed using HLS.
4. You can view the video on the homepage.
5. You can also view your watch history and resume watching videos from where you left off.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have any improvements to offer. Frontend implementation is not yet complete, so any help in that area would be greatly appreciated.

## License

This project is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT).
