const expenseForm = document.getElementById("expense-form");
const expenseNameInput = document.getElementById("expense-name");
const expenseAmountInput = document.getElementById("expense-amount");
const expenseCategoryInput = document.getElementById("expense-category");
const expenseList = document.getElementById("expense-list");
const totalAmount = document.getElementById("total-amount");
const filterCategory = document.getElementById("filter-category");

let expenses = JSON.parse(localStorage.getItem("expenses")) || [];

function saveExpenses() {
  localStorage.setItem("expenses", JSON.stringify(expenses));
}

function calculateTotal(filteredExpenses = expenses) {
  const total = filteredExpenses.reduce((sum, expense) => {
    return sum + expense.amount;
  }, 0);

  totalAmount.textContent = total.toFixed(2);
}

function renderExpenses(expensesToRender = expenses) {
  expenseList.innerHTML = "";

  if (expensesToRender.length === 0) {
    expenseList.innerHTML = "<li>No expenses found.</li>";
    calculateTotal([]);
    return;
  }

  expensesToRender.forEach((expense) => {
    const li = document.createElement("li");
    li.classList.add("expense-item");

    li.innerHTML = `
      <div class="expense-info">
        <span class="expense-name">${expense.name}</span>
        <span class="expense-category">${expense.category}</span>
      </div>
      <span class="expense-amount">£${expense.amount.toFixed(2)}</span>
      <button class="delete-btn" data-id="${expense.id}">Delete</button>
    `;

    expenseList.appendChild(li);
  });

  calculateTotal(expensesToRender);
}

function addExpense(event) {
  event.preventDefault();

  const name = expenseNameInput.value.trim();
  const amount = parseFloat(expenseAmountInput.value);
  const category = expenseCategoryInput.value;

  if (!name || isNaN(amount) || amount <= 0 || !category) {
    alert("Please enter valid expense details.");
    return;
  }

  const newExpense = {
    id: Date.now(),
    name,
    amount,
    category
  };

  expenses.push(newExpense);
  saveExpenses();
  applyFilter();

  expenseForm.reset();
}

function deleteExpense(event) {
  if (!event.target.classList.contains("delete-btn")) {
    return;
  }

  const expenseId = Number(event.target.dataset.id);

  expenses = expenses.filter((expense) => expense.id !== expenseId);
  saveExpenses();
  applyFilter();
}

function applyFilter() {
  const selectedCategory = filterCategory.value;

  if (selectedCategory === "All") {
    renderExpenses(expenses);
    return;
  }

  const filteredExpenses = expenses.filter((expense) => {
    return expense.category === selectedCategory;
  });

  renderExpenses(filteredExpenses);
}

expenseForm.addEventListener("submit", addExpense);
expenseList.addEventListener("click", deleteExpense);
filterCategory.addEventListener("change", applyFilter);

renderExpenses();