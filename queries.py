queries = {

"1": {
"title": "Show all users",
"sql": "SELECT * FROM users"
},

"2": {
"title": "Show all accounts",
"sql": "SELECT * FROM accounts"
},

"3": {
"title": "Show all categories",
"sql": "SELECT * FROM categories"
},

"4": {
"title": "Show all expenses",
"sql": "SELECT * FROM expenses"
},

"5": {
"title": "Show all income records",
"sql": "SELECT * FROM income"
},

"6": {
"title": "Show all budgets",
"sql": "SELECT * FROM budgets"
},

"7": {
"title": "Show all transactions",
"sql": "SELECT * FROM transactions"
},

"8": {
"title": "Show all savings goals",
"sql": "SELECT * FROM goals"
},

"9": {
"title": "Show users with their account balances",
"sql": """
SELECT users.name, accounts.account_type, accounts.balance
FROM users
JOIN accounts ON users.user_id = accounts.user_id
"""
},

"10": {
"title": "Show total expense amount",
"sql": "SELECT SUM(amount) AS total_expense FROM expenses"
},

"11": {
"title": "Show average expense amount",
"sql": "SELECT AVG(amount) AS average_expense FROM expenses"
},

"12": {
"title": "Show highest income",
"sql": "SELECT MAX(amount) AS highest_income FROM income"
},

"13": {
"title": "Show lowest account balance",
"sql": "SELECT MIN(balance) AS lowest_balance FROM accounts"
},

"14": {
"title": "Show total expense per user",
"sql": """
SELECT users.name, SUM(expenses.amount) AS total_spent
FROM users
JOIN expenses ON users.user_id = expenses.user_id
GROUP BY users.name
"""
},

"15": {
"title": "Show total income per user",
"sql": """
SELECT users.name, SUM(income.amount) AS total_income
FROM users
JOIN income ON users.user_id = income.user_id
GROUP BY users.name
"""
},

"16": {
"title": "Show expenses greater than 1000",
"sql": "SELECT * FROM expenses WHERE amount > 1000"
},

"17": {
"title": "Show accounts with balance above average",
"sql": """
SELECT * FROM accounts
WHERE balance > (SELECT AVG(balance) FROM accounts)
"""
},

"18": {
"title": "Show highest expense",
"sql": "SELECT * FROM expenses ORDER BY amount DESC LIMIT 1"
},

"19": {
"title": "Show lowest income",
"sql": "SELECT * FROM income ORDER BY amount ASC LIMIT 1"
},

"20": {
"title": "Show goal remaining amount",
"sql": """
SELECT user_id, target_amount - current_amount AS remaining_amount
FROM goals
"""
},

"21": {
"title": "Count total users",
"sql": "SELECT COUNT(*) AS total_users FROM users"
},

"22": {
"title": "Count total expenses",
"sql": "SELECT COUNT(*) AS total_expenses FROM expenses"
},

"23": {
"title": "Show distinct account types",
"sql": "SELECT DISTINCT account_type FROM accounts"
},

"24": {
"title": "Show expenses between 500 and 1500",
"sql": "SELECT * FROM expenses WHERE amount BETWEEN 500 AND 1500"
},

"25": {
"title": "Show users whose name starts with User1",
"sql": "SELECT * FROM users WHERE name LIKE 'User1%'"
}

}