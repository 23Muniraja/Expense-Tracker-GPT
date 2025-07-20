document.addEventListener("DOMContentLoaded", function () {
    // Parse JSON data from HTML
    const yearlyData = JSON.parse(document.getElementById("yearly-data").textContent);
    const monthlyData = JSON.parse(document.getElementById("monthly-data").textContent);
    const categoryData = JSON.parse(document.getElementById("category-data").textContent);
    const topExpenses = JSON.parse(document.getElementById("top-expenses").textContent);
    const avgMonthlySpend = document.getElementById("avg-monthly").textContent;

    // Yearly Bar Chart
    new Chart(document.getElementById("yearlyChart"), {
        type: "bar",
        data: {
            labels: yearlyData.map(row => row.year),
            datasets: [{
                label: "Yearly Expense",
                data: yearlyData.map(row => row.total),
                backgroundColor: "#4e73df"
            }]
        }
    });

    // Monthly Line Chart
    new Chart(document.getElementById("monthlyChart"), {
        type: "line",
        data: {
            labels: monthlyData.map(row => row.month),
            datasets: [{
                label: "Monthly Expense",
                data: monthlyData.map(row => row.total),
                fill: false,
                borderColor: "#1cc88a"
            }]
        }
    });

    // Category Pie Chart
    new Chart(document.getElementById("categoryChart"), {
        type: "pie",
        data: {
            labels: categoryData.map(row => row.category),
            datasets: [{
                data: categoryData.map(row => row.total),
                backgroundColor: ["#f6c23e", "#e74a3b", "#36b9cc", "#1cc88a", "#4e73df"]
            }]
        }
    });

    // Top 5 Expenses Bar
    new Chart(document.getElementById("topExpensesChart"), {
        type: "bar",
        data: {
            labels: topExpenses.map(row => `${row.expense_date} (${row.category})`),
            datasets: [{
                label: "Top 5 Expenses",
                data: topExpenses.map(row => row.amount),
                backgroundColor: "#e74a3b"
            }]
        }
    });

    // Average Monthly Spend (Text Card)
    document.getElementById("avgSpendValue").textContent = `₹ ${avgMonthlySpend}`;
});
