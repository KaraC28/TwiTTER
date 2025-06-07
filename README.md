# TwiTTER
A website hosted on PythonAnywhere that simulates a social media platform.
# General Info
Languages: HTML, CSS, Javascript, Python
AWS Services: IAM, S3, DynamoDB
- This project uses flask for app routing
- Users can sign up for a new account to the website using their email, username, and password, this information is stored in an AWS DynamoDB table
- The webpage notifies the user if they are missing @ and/or . in their email
- Users can login to their account using their email and password, this information is located through the user's unique id
- Logging in gives an option to remember the user through cookies
- Users can view their own posts and add new posts to their profile, user's post information is stored in an AWS DynamoDB table
- Users can upload and update their profile picture, this information is stored in an AWS S3 table
- Clicking on the feed link allows the user to view the ten most recent posts
- Commenting on another user/s reply will take the user to another page and display other user's replies, reply information is stored in an AWS DynamoDB table and are identified through the parent ids of posts
- Clicking on a user's username will take the user to the other user's page, but will not allow the user to edit or change the pfp of the ohter user
- Clicking on the logout link will logout the user and take them to the home page, which displays a login link and signup link
# Images
![Image](https://github.com/user-attachments/assets/1a00a282-837f-4862-a257-c0654a2c1f3b) 

![Image](https://github.com/user-attachments/assets/1fab384e-8862-4af9-bfd1-7d3e7d594436)

![Image](https://github.com/user-attachments/assets/a1434c92-3046-4617-bd55-c781723c26b8)

![Image](https://github.com/user-attachments/assets/9f268d2f-5f43-4b93-ac8a-5189525d57f4) 

![Image](https://github.com/user-attachments/assets/0bbe3127-bdb3-4d5b-ba71-eaf91b92be09) 

![Image](https://github.com/user-attachments/assets/0233c94b-e5b1-4613-8577-469005c475c3)
# Known Issues
- Request bug for uploading image
- Stored pfp doesn't appear in profile page
# Collaborators
Nowah Stewart, Pace University Student
