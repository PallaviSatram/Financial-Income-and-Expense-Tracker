function runQuery(id)
{
    let outputDiv = document.getElementById("output-" + id);

    // If already showing → hide it
    if (outputDiv.innerHTML.trim() !== "") {
        outputDiv.innerHTML = "";
        return;
    }

    // Otherwise fetch and show
    fetch("/run_query/" + id)
    .then(res => res.json())
    .then(data => {

        let html = "";

        if(data.length > 0)
        {
            html += "<table>";

            html += "<tr>";
            Object.keys(data[0]).forEach(key=>{
                html += "<th>"+key+"</th>";
            });
            html += "</tr>";

           data.forEach(row=>{
    html += "<tr>";

    Object.entries(row).forEach(([key,val])=>{
        html += "<td>"+val+"</td>";
    });

    // Only for users table
    if(row.user_id){

        html += `<td>

        <a href="/edit_user/${row.user_id}">
            <button class="edit-btn">Edit</button>
        </a>

        <button class="delete-btn" onclick="deleteUser(${row.user_id})">
            Delete
        </button>

        </td>`;
    }

    html += "</tr>";
});

            html += "</table>";
        }
        else
        {
            html = "<p>No data returned.</p>";
        }

        outputDiv.innerHTML = html;
    });
}

function deleteUser(id){

    let confirmDelete = confirm("Are you sure you want to delete this user?");

    if(confirmDelete){
        window.location.href = "/delete_user/" + id;
    }

}
function createTable(data){

let html="<table>";

if(data.length>0){

html+="<tr>";

Object.keys(data[0]).forEach(key=>{
html+="<th>"+key+"</th>";
});

html+="<th>Action</th></tr>";

data.forEach(row=>{

html+="<tr>";

Object.values(row).forEach(val=>{
html+="<td>"+val+"</td>";
});

html+=`
<td>
<button class="delete-btn" onclick="deleteExpense(${row.expense_id})">
Delete
</button>
</td>
`;

html+="</tr>";

});

}

html+="</table>";

return html;

}
function loadTotalExpense(){

fetch("/total_expense")
.then(res => res.json())
.then(data => {

document.getElementById("totalExpenseCard").innerText =
"₹ " + data.total

})

}

function deleteExpense(id){

let confirmDelete = confirm("Are you sure you want to delete this expense?");

if(!confirmDelete) return;

fetch("/delete_expense/" + id, {
method: "DELETE"
})
.then(res => res.json())
.then(() => {

    // reload expenses table
    toggleExpenses();

    // update total expense card
    loadTotalExpense();

});

}

function toggleExpenses(){

let div=document.getElementById("expenses")

if(div.innerHTML!=""){
div.innerHTML=""
return
}

fetch("/user_expenses")
.then(res=>res.json())
.then(data=>{
div.innerHTML=createTable(data)
})

}


// Load total expense
fetch("/total_expense")
.then(res=>res.json())
.then(data=>{
document.getElementById("totalExpense").innerText =
"₹ " + (data.total || 0)
})



// Load categories
fetch("/categories")
.then(res=>res.json())
.then(data=>{

let html=""

data.forEach(cat=>{
html+=`<button class="category-btn"
onclick="showCategory('${cat.category}')">
${cat.category}
</button>`
})

document.getElementById("categoriesList").innerHTML=html

})




// Show category details
function showCategory(category){

fetch("/category_details/"+category)
.then(res=>res.json())
.then(data=>{

let text="<p><b>"+category+"</b></p>"

data.forEach(item=>{
text+=`<p>Spent ₹${item.amount} on ${item.date}</p>`
})

document.getElementById("categoryDetails").innerHTML=text

})

}

function loadMonthlyExpense(){

let month = document.getElementById("monthSelect").value

if(month==""){
document.getElementById("monthlyTable").innerHTML=""
return
}

fetch("/monthly_expense/"+month)
.then(res=>res.json())
.then(data=>{

let html="<table>"

if(data.length>0){

html+="<tr><th>Category</th><th>Total Amount</th></tr>"

data.forEach(row=>{
html+=`<tr>
<td>${row.category}</td>
<td>₹ ${row.total}</td>
</tr>`
})

}

else{

html="<p>No expenses for this month</p>"

}

html+="</table>"

document.getElementById("monthlyTable").innerHTML=html

})

}

function loadBalance(){

fetch("/balance")
.then(res=>res.json())
.then(data=>{

document.getElementById("totalIncome").innerText = "₹ " + data.income

document.getElementById("totalExpense").innerText = "₹ " + data.expense

document.getElementById("balanceAmount").innerText = "₹ " + data.balance


if(data.balance < 0){

document.getElementById("balanceAlert").innerText =
"⚠ Expense exceeds income! Amount not enough."

document.getElementById("balanceAlert").style.color = "red"

}else{

document.getElementById("balanceAlert").innerText =
"✔ Your balance is healthy."

document.getElementById("balanceAlert").style.color = "green"

}

})

}
function toggleIncome(){

let div = document.getElementById("incomeTable")

if(div.innerHTML != ""){
div.innerHTML = ""
return
}

fetch("/user_income")
.then(res => res.json())
.then(data => {

if(data.length === 0){
div.innerHTML = "<p>No income history available</p>"
return
}

div.innerHTML = createTable(data)

})

}

loadBalance();
loadTotalExpense();