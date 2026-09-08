# Import libraries
from flask import Flask, redirect, request, render_template, url_for
# Instantiate Flask functionality
app = Flask(__name__)
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
# Read operation
@app.route("/")
def get_transactions():
    # Calculate total balance to display at the bottom of the table
    balance = sum(transaction['amount'] for transaction in transactions)
    return render_template("transactions.html", transactions=transactions, balance=balance)
# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        # create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(transaction)
        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    # Render the form template to display the add transaction form (GET request)
    return render_template("form.html")
# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']  # Get the 'date' field value
        amount = float(request.form['amount'])  # Get the 'amount' field value
        # Find the transaction with the matching ID and update the values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break  # Exits the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)
    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404
# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove transaction
            return redirect(url_for("get_transactions"))
    # If no transaction with the matching ID is found, return a 404 error
    return {"message": "Transaction not found"}, 404
# Search operation: Route to search transactions within an amount range
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == 'POST':
        # Retrieve min and max amount values from the form and convert to float
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        # Filter transactions whose amount falls within the specified range
        filtered_transactions = [
            transaction for transaction in transactions
            if min_amount <= transaction['amount'] <= max_amount
        ]
        balance = sum(transaction['amount'] for transaction in filtered_transactions)
        # Render the transactions template with the filtered results
        return render_template("transactions.html", transactions=filtered_transactions, balance=balance)
    # If GET, render the search form
    return render_template("search.html")
# Balance operation: Route to calculate and return the total balance
@app.route("/balance")
def total_balance():
    # Sum the amount values of all transactions
    balance = sum(transaction['amount'] for transaction in transactions)
    return f"Total Balance: {balance}"
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
