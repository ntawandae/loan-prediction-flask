from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt, joblib
from flask_migrate import Migrate
import numpy as np
import logging
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import timedelta




with open("model.joblib", 'rb') as file:
    model = joblib.load(file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)
migrate=Migrate(app, db)
app.secret_key = 'secret_key'


login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view endpoint


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(), default='User')
    authenticated = db.Column(db.Boolean, default=False)
    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

@app.route('/')
def home():
    labels = [
        'Newlywed Grants',
        'Student Loans',
        'Personal Loan',
        'Real Estate',
        'Unemployment Grants',
        'Mortgage',
        'assets accumulation'
    ]

    data = [0, 10, 15, 8, 22, 18, 25]

    # Log the length of data array to the console for debugging
    print(f"Data array length: {len(data)}")

    # Return the components to the HTML template
    return render_template(
        template_name_or_list='dashboard.html',
        data=data,
        labels=labels,
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)  # Use the plain text password here
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

from flask import url_for
from flask_login import login_user, logout_user

# Example logging statements
import logging
logging.basicConfig(level=logging.INFO)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            user.authenticated = True
            db.session.commit()

            login_user(user)
            flash('Login successful!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('userprofile'))
        else:
            flash('Incorrect password or invalid email. Please try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    current_user.authenticated = False
    db.session.commit()

    logout_user()
    flash('Logout successful!', 'success')

    return redirect('/login')

from flask_login import current_user

@app.route('/userprofile')
@login_required
def userprofile():
    return render_template('user-profile.html', user=current_user)


    return redirect('/login')


from flask_login import login_required


@app.route('/admin_profile')
@login_required
def admin_profile():
    applications = LoanApplication.query.all()
    return render_template('index.html', user=current_user,  applications=applications)


from flask_login import login_required
@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    return render_template("prediction.html")


class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_initial = db.Column(db.String(10))
    last_name = db.Column(db.String(50), nullable=False)
    gender= db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    contact_number = db.Column(db.String(50), nullable=False)
    home_address= db.Column(db.String(50), nullable=False)
    education = db.Column(db.String(50), nullable=False)
    Employment_status = db.Column(db.String(50), nullable=False)
    Employer_name= db.Column(db.String(50), nullable=False)
    Salary= db.Column(db.Integer(), nullable=False)
    credit_score= db.Column(db.Numeric(3, 4),nullable=False)
    marital_status = db.Column(db.String(50), nullable=False)
    spouse_name = db.Column(db.String(50))
    spouse_employment_status= db.Column(db.String(50))
    spouse_salary = db.Column(db.Integer())
    spouse_employer = db.Column(db.String(50))
    dependents = db.Column(db.String(50), nullable=False)
    property_location = db.Column(db.String(50), nullable=False)
    loan_amount = db.Column(db.Integer(), nullable=False)
    loan_term_length= db.Column(db.Integer(), nullable=False)
    declaration= db.Column(db.String(50))
    loan_applicant_userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('loan_applications', lazy=True))
    
@app.route('/loan_application', methods=['POST'])
@login_required
def loan_application():
    if request.method == 'POST':
        # Get data from the form
        first_name = request.form['first_name']
        middle_initial = request.form['middle_initial']
        last_name = request.form['last_name']
        gender = request.form['gender']
        email = request.form['email']
        contact_number = request.form['telephone']
        home_address = request.form['home_address']
        education = request.form['education']
        Salary = request.form['ApplicantIncome']
        Employment_status = request.form['employed']
        Employer_name = request.form['company_name']
        credit_score = request.form['credit']
        marital_status = request.form['married']
        spouse_name = request.form['spouse']
        spouse_employment_status = request.form['spouse_employed']
        spouse_salary = request.form['CoapplicantIncome']
        spouse_employer = request.form['spouse_company_name']
        dependents = request.form['dependents']
        property_location = request.form['area']
        loan_amount = request.form['LoanAmount']
        loan_term_length = request.form['Loan_Amount_Term']
        declaration = request.form['declaration']

        # Make predictions
        prediction = predict_loan_approval(
            gender, marital_status, dependents, education, Employment_status,
            float(credit_score), property_location, float(Salary),
            float(spouse_salary), float(loan_amount),
            float(loan_term_length)
        )

        # Check if the prediction is true (approved)
        if prediction:
            # Create a new LoanApplication instance
            new_application = LoanApplication(
                first_name=first_name, middle_initial=middle_initial, last_name=last_name,
                gender=gender, email=email, contact_number=contact_number,
                home_address=home_address, education=education, Salary=Salary,
                Employment_status=Employment_status, Employer_name=Employer_name,
                credit_score=credit_score, marital_status=marital_status,
                spouse_name=spouse_name, spouse_employment_status=spouse_employment_status,
                spouse_salary=spouse_salary, spouse_employer=spouse_employer,
                dependents=dependents, property_location=property_location,
                loan_amount=loan_amount, loan_term_length=loan_term_length,
                declaration=declaration,
                loan_applicant_userid=current_user.id  # Assuming you have the user ID
            )

            # Add the new application to the database
            db.session.add(new_application)
            db.session.commit()
            flash('Loan application approved and saved!', 'success')

            # Redirect to view_applications page
            return redirect(url_for('userprofile'))
        else:
            flash('Loan application not approved.', 'info')

            # Redirect to userprofile page
            return redirect(url_for('predict'))

    # Handle cases where the request method is not POST
    flash('Invalid request method.', 'error')
    return redirect(url_for('userprofile'))

def predict_loan_approval(gender, married, dependents, education, employed, credit, area, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term):
    
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0


        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

    
    # Adjust this logic based on your model's output format and threshold
    prediction = model.predict([[credit, ApplicantIncomelog, LoanAmountlog,
                                 Loan_Amount_Termlog, totalincomelog, male,
                                 married_yes, dependents_1, dependents_2,
                                 dependents_3, not_graduate, employed_yes,
                                 semiurban, urban]])

    return prediction == "Y"


@app.route('/view_applications', methods=['GET'])
def view_applications():
    # Retrieve all LoanApplication records from the database  for the logged-in user
    user_applications = LoanApplication.query.all()


    # Render a template to display the user's records
    return render_template('view_applications.html', applications=user_applications)

 
if __name__ == "__main__":
    app.run(debug=True)
