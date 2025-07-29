
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#run-using-docker">Run using Docker</a></li>
        <li><a href="#run-locally">Run Locally</a></li>
      </ul>
    </li>
  </ol>
</details>



## About The Project

<img width="830" height="480" alt="image" src="https://github.com/user-attachments/assets/1428f6d1-c5d3-436b-af7f-bf71791329f9" />

Planning and managing your tasks is the key to success.
This project helps you achieve your goals more efficiently by providing a simple, structured way to stay on track.

* Create projects
* Add tasks
* Set priorities
* Set deadlines
* Monitor progress—all in one place.
No distractions, no unnecessary features—just clear, focused task planning and tracking.

## Getting Started

### Run using Docker
   ```sh
   docker-compose up
   ```

You should then be able to open your browser on http://localhost:8000 and see sign in page.

### Run Locally

Assuming you use virtualenv, follow these steps to download and run the application in this directory:

   ```sh
   git clone git@github.com:YevheniyEvt/task_app.git
   cd task_app
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

Now we need to create the database tables and an admin user. Run the following and when prompted to create a superuser choose yes and follow the instructions:

   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   ```

Finally, run the Django development server:

   ```sh
   python manage.py runserver
   ```

You should then be able to open your browser on http://localhost:8000 and see sign in page.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
