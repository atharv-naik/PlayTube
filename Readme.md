# YouTube-like Video-on-Demand Platform in Django

This project is a Video-on-Demand (VOD) platform developed using Django, providing features similar to those found on YouTube. It allows users to upload videos, which are then transcoded and streamed using HLS (HTTP Live Streaming). The project also includes user authentication, social logins, video playback tracking, and more.

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
   - Google social login is integrated using `django-allauth` for a seamless experience.

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
    python3 -m venv venv

    source venv/bin/activate

    ```
3. Install the dependencies:

   ```bash
    pip install -r requirements.txt

    ```
4. Configure your Amazon S3 credentials and other settings in `settings.py`.

5. Run the migrations:

   ```bash
    python manage.py migrate

    ```
6. Create a superuser:

   ```bash
    python manage.py createsuperuser

    ```
7. Run the development server:

   ```bash
    python manage.py runserver

    ```
8. Run the Celery worker:

   ```bash
    celery -A YouTube worker -l info

    ```
9. Run the Celery beat scheduler:

   ```bash
    celery -A YouTube beat -l info

    ```
10. Run the Redis server:

    ```bash
    redis-server

    ```
11. Navigate to `http://localhost:8000/` in your browser.

## Usage

1. Register a new user account or login using an existing one.
2. Upload a video using the upload form.
3. Once the video is uploaded, it will be transcoded and streamed using HLS.
4. You can view the video on the homepage.
5. You can also view your watch history and resume watching videos from where you left off.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have any improvements to offer.

## License

This project is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT).
