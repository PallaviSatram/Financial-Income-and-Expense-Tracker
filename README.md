**Financial Expense & Income Tracker**

A web-based Financial Expense & Income Tracker that helps users manage their personal finances efficiently. The system allows users to record income and expenses, analyze financial activity, and monitor their balance through an interactive dashboard.

This project demonstrates the practical implementation of Database Management System (DBMS) concepts integrated with web development technologies.

**Features**

- User Registration and Login
- Add and manage expenses
- Add and manage income
- View expense and income history
- Financial summary showing:
- Total Income
- Total Expenses
- Balance
- Category-wise expense tracking
- Monthly expense analysis
- User profile management
- Delete expenses and income records
- Secure session-based authentication

**Tech Stack**
Frontend
- HTML
- CSS
- JavaScript

Backend
- Python
- Flask

Database
- SQLite
  
**Database Design**
The system uses a relational database structure consisting of four main tables.
Users Table
- user_id (Primary Key)
- name
- email
- password
  
Expenses Table
- expense_id (Primary Key)
- user_id (Foreign Key)
- category_id (Foreign Key)
- amount
- date

Income Table
- income_id (Primary Key)
- user_id (Foreign Key)
- source
- amount
- date

Category Table
- category_id (Primary Key)
- category_name
- created_at

**System Architecture**

The system follows a three-layer architecture:
- Presentation Layer
Frontend developed using HTML, CSS, and JavaScript for user interaction.
- Application Layer
Python Flask handles application logic, user authentication, and communication between frontend and database.
- Database Layer
SQLite stores all application data including user details, expenses, income records, and categories.

**Project Structure**
ExpenseTracker
│
├── app.py
├── database.py
├── queries.py
├── expense.db
│
├── templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   └── financial_summary.html
│
├── static
│   ├── style.css
│   └── script.js
│
└── README.md

**Installation**
1 Clone the repository
git clone https://github.com/PallaviSatram/Financial-Income-and-Expense-Tracker/
2 Navigate to the project folder
cd expense-tracker
3 Install dependencies
pip install flask
4 Run the application
python app.py
5 Open the browser
http://127.0.0.1:5000

**How It Works**

- Users register and create an account.
- Users log in using their credentials.
- After login, users access the dashboard.
- Users can add expenses and income records.
- The system stores data in the SQLite database.
- The dashboard displays financial summaries and analytics.
- Users can delete records or update profile information.

  **This project is developed for educational purposes as part of a DBMS course project.**
