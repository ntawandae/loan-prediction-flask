# loan-prediction-flask

The project is a Flask web application featuring user authentication, role-based access control, and loan eligibility prediction using a machine learning algorithm. Users can register, log in, and log out, with secure password hashing. Each user has a specific role (e.g., admin or user), and the application displays different dashboards based on their role.
In addition to authentication, the application incorporates a machine learning algorithm to assess a user's eligibility for a loan. Upon login, the system predicts loan approval based on user inputs. If the prediction is positive, the user's loan application details are saved to a SQLite database using Flask-SQLAlchemy. If the prediction is negative, the user receives a notification.
The project employs Flask-Login for user session management, bcrypt for password hashing, and Flask-Migrate for database migrations. It serves as an example of integrating machine learning functionality within a web application for loan eligibility determination.

**sign-up window**
![fe new sign-up](https://github.com/ntawandae/loan-prediction-flask/assets/56553042/1b41e72e-211b-4938-8c8d-47feaf8fcf7b)
**login window**
![fe new login](https://github.com/ntawandae/loan-prediction-flask/assets/56553042/ec8610ec-ec17-427a-95c5-7995ecaf1ffb)
**Dashboard**
![msg dashboard](https://github.com/ntawandae/loan-prediction-flask/assets/56553042/dee46e1c-a659-4460-9efb-f87cc4ddb0fe)
**#loan application**(the eligibility test is carried here, if user is eligible the information is saved and made available to admin who will give final decision to grant or reject the loan
![fe application](https://github.com/ntawandae/loan-prediction-flask/assets/56553042/c6bca914-6d3a-47cc-a054-74a99376689d)
**user profile view**
![fe up](https://github.com/ntawandae/loan-prediction-flask/assets/56553042/e89bb0e2-0f4f-4de3-8742-bac8e83d93f1)
**admin view** of all received loan applications
![fe adminview](https://github.com/ntawandae/loan-prediction-flask/assets/56553042/31c0aab2-6e42-4dec-89b1-889c6f36b59d)
**search loan window**
![fe search](https://github.com/ntawandae/loan-prediction-flask/assets/56553042/3a0da9d7-0663-4c14-9ef6-da1fade6a99e)

****Usage****


firstly activate the virtual envronment for this to work then run
python app.py

