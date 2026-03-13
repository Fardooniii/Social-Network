# Network – Social Media Web App

Network is a social networking web application built using **Django, Python, JavaScript, HTML, and CSS**. It allows users to interact in a way similar to modern social media platforms, with posts, likes, follows, and user profiles.  

Users can **register, log in, and log out**, and once signed in they can:  
- **Create new text-based posts** and share them with everyone on the platform.  
- **View all posts** from all users in reverse chronological order, including the post content, author, timestamp, and number of likes.  
- **Like and unlike posts** dynamically using JavaScript, without needing to reload the page.  
- **Edit their own posts** inline, with changes saved immediately using JavaScript.  
- **Visit user profile pages**, showing a user’s posts, followers, and following counts.  
- **Follow or unfollow other users**, allowing them to see only the posts from users they follow in the “Following” feed.  
- **Browse posts with pagination**, showing 10 posts per page with “Next” and “Previous” buttons for easy navigation.  

The app also adjusts its layout depending on whether a user is signed in, showing appropriate navigation links and options. This makes the platform secure and user-friendly, ensuring that users can only edit their own posts and interact with content as intended.  

**How to run the project:**  
- Download and unzip the distribution code  
- Open terminal and `cd` into the `project4` directory  
- Run `python manage.py makemigrations`  
- Run `python manage.py migrate`  
- Run `python manage.py runserver`  
- Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to start using the app
