const form =
    document.getElementById("expense-form");

const submitButton =
    document.getElementById("submit-button");

const cancelEditButton =
    document.getElementById("cancel-edit-button");

const initialDataElement =
    document.getElementById("initial-data");

const generateAIButton =
    document.getElementById("generate-ai-button");

const aiLoading =
    document.getElementById("ai-loading");

const aiResult =
    document.getElementById("ai-result");

const categorySort =
    document.getElementById("category-sort");


window.initialCategoryTotals =
    JSON.parse(
        initialDataElement.dataset.categoryTotals
    );

window.initialCategoryPercentages =
    JSON.parse(
        initialDataElement.dataset.categoryPercentages
    );


let editingExpenseId = null;

let categoryChart = null;

let currentCategoryTotals =
    window.initialCategoryTotals;

let currentCategoryPercentages =
    window.initialCategoryPercentages;


// --------------------------------
// FORMAT MONEY
// --------------------------------

function formatMoney(value) {

    return Number(value).toLocaleString(
        "en-US",
        {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }
    );
}


// --------------------------------
// INITIAL PAGE
// --------------------------------

createCategoryChart(
    window.initialCategoryTotals
);

updateCategoryBreakdown(
    window.initialCategoryTotals,
    window.initialCategoryPercentages
);


// --------------------------------
// CATEGORY SORT
// --------------------------------

categorySort.addEventListener(
    "change",
    function () {

        updateCategoryBreakdown(
            currentCategoryTotals,
            currentCategoryPercentages
        );
    }
);


// --------------------------------
// ADD / UPDATE EXPENSE
// --------------------------------

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const formData =
            new FormData(form);


        const expenseData = {
            name: formData.get("name"),
            amount: formData.get("amount"),
            frequency: formData.get("frequency"),
            category: formData.get("category")
        };


        let url =
            "/add-expense";

        let method =
            "POST";


        if (editingExpenseId !== null) {

            url =
                `/update-expense/${editingExpenseId}`;

            method =
                "PUT";
        }


        const response =
            await fetch(
                url,
                {
                    method: method,

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(expenseData)
                }
            );


        if (!response.ok) {

            console.error(
                "Could not save expense"
            );

            return;
        }


        const data =
            await response.json();


        updatePage(data);

        resetForm();
    }
);


// --------------------------------
// EDIT EXPENSE
// --------------------------------

document.addEventListener(
    "click",
    function (event) {

        const editButton =
            event.target.closest(
                ".edit-button"
            );


        if (!editButton) {
            return;
        }


        editingExpenseId =
            editButton.dataset.id;


        document.getElementById(
            "expense-name"
        ).value =
            editButton.dataset.name;


        document.getElementById(
            "expense-amount"
        ).value =
            editButton.dataset.amount;


        document.getElementById(
            "expense-frequency"
        ).value =
            editButton.dataset.frequency;


        document.getElementById(
            "expense-category"
        ).value =
            editButton.dataset.category;


        submitButton.textContent =
            "Save Changes";


        cancelEditButton.classList.remove(
            "hidden"
        );
    }
);


// --------------------------------
// CANCEL EDIT
// --------------------------------

cancelEditButton.addEventListener(
    "click",
    function () {

        resetForm();
    }
);


// --------------------------------
// DELETE EXPENSE
// --------------------------------

document.addEventListener(
    "click",
    function (event) {

        const deleteButton =
            event.target.closest(
                ".delete-button"
            );


        if (!deleteButton) {
            return;
        }


        deleteExpense(
            deleteButton.dataset.id
        );
    }
);


async function deleteExpense(
    expenseId
) {

    const response =
        await fetch(
            `/delete-expense/${expenseId}`,
            {
                method: "DELETE"
            }
        );


    if (!response.ok) {

        console.error(
            "Could not delete expense"
        );

        return;
    }


    const data =
        await response.json();


    updatePage(data);

    resetForm();
}


// --------------------------------
// RESET FORM
// --------------------------------

function resetForm() {

    form.reset();

    editingExpenseId =
        null;

    submitButton.textContent =
        "Add Expense";

    cancelEditButton.classList.add(
        "hidden"
    );
}


// --------------------------------
// UPDATE PAGE
// --------------------------------

function updatePage(data) {

    updateExpenseTable(
        data.expenses
    );

    updateMetrics(data);

    updateInsight(
        data.largest_expense
    );

    updateAnalysis(
        data.category_totals,
        data.category_percentages
    );
}


// --------------------------------
// EXPENSE TABLE
// --------------------------------

function updateExpenseTable(
    expenses
) {

    const tableBody =
        document.getElementById(
            "expense-table-body"
        );


    tableBody.innerHTML =
        "";


    if (expenses.length === 0) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="7">
                    No recurring expenses added yet.
                </td>
            </tr>
        `;

        return;
    }


    expenses.forEach(
        function (
            expense,
            index
        ) {

            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `

                <td>
                    ${index + 1}
                </td>

                <td>
                    ${expense.name}
                </td>

                <td>
                    $${formatMoney(
                        expense.amount
                    )}
                </td>

                <td>
                    ${expense.frequency}
                </td>

                <td>
                    ${expense.category}
                </td>

                <td>
                    $${formatMoney(
                        expense.monthly_cost
                    )}
                </td>

                <td class="action-buttons">

                    <button
                        type="button"
                        class="edit-button"
                        data-id="${expense.id}"
                        data-name="${expense.name}"
                        data-amount="${expense.amount}"
                        data-frequency="${expense.frequency}"
                        data-category="${expense.category}"
                        title="Edit expense"
                    >
                        ✎
                    </button>


                    <button
                        type="button"
                        class="delete-button"
                        data-id="${expense.id}"
                        title="Delete expense"
                    >
                        🗑
                    </button>

                </td>
            `;


            tableBody.appendChild(
                row
            );
        }
    );
}


// --------------------------------
// METRICS
// --------------------------------

function updateMetrics(
    data
) {

    document.getElementById(
        "monthly-total"
    ).textContent =
        `$${formatMoney(
            data.total_monthly
        )}`;


    document.getElementById(
        "yearly-total"
    ).textContent =
        `$${formatMoney(
            data.total_yearly
        )}`;


    document.getElementById(
        "active-expenses"
    ).textContent =
        data.active_expenses;
}


// --------------------------------
// QUICK INSIGHT
// --------------------------------

function updateInsight(
    largestExpense
) {

    const insightCard =
        document.getElementById(
            "insight-card"
        );


    if (largestExpense) {

        insightCard.innerHTML = `

            <p class="eyebrow">
                QUICK INSIGHT
            </p>

            <h3>
                Your largest recurring expense is

                <span>
                    ${largestExpense.name}
                </span>.
            </h3>

            <p>
                It costs you approximately

                $${formatMoney(
                    largestExpense.monthly_cost
                )}

                per month.
            </p>
        `;

    } else {

        insightCard.innerHTML = `

            <p class="eyebrow">
                QUICK INSIGHT
            </p>

            <h3>
                Add your first expense
                to see an insight.
            </h3>

            <p>
                Adisade will help you understand
                where your recurring money is going.
            </p>
        `;
    }
}


// --------------------------------
// ANALYSIS
// --------------------------------

function updateAnalysis(
    categoryTotals,
    categoryPercentages
) {

    currentCategoryTotals =
        categoryTotals;

    currentCategoryPercentages =
        categoryPercentages;


    updateCategoryBreakdown(
        categoryTotals,
        categoryPercentages
    );

    createCategoryChart(
        categoryTotals
    );

    updateSavingsCard(
        categoryTotals
    );
}


// --------------------------------
// CATEGORY BREAKDOWN + SORT
// --------------------------------

function updateCategoryBreakdown(
    totals,
    percentages
) {

    const container =
        document.getElementById(
            "category-breakdown"
        );


    container.innerHTML =
        "";


    let categories =
        Object.keys(
            totals
        );


    if (categories.length === 0) {

        container.innerHTML = `
            <p>
                Add expenses to see your spending breakdown.
            </p>
        `;

        return;
    }


    const sortValue =
        categorySort.value;


    if (
        sortValue ===
        "low-to-high"
    ) {

        categories.sort(
            (a, b) =>
                totals[a] -
                totals[b]
        );

    } else {

        categories.sort(
            (a, b) =>
                totals[b] -
                totals[a]
        );
    }


    categories.forEach(
        function (
            category
        ) {

            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "category-row";


            row.innerHTML = `

                <div>

                    <strong>
                        ${category}
                    </strong>

                    <span>
                        ${Number(
                            percentages[
                                category
                            ]
                        ).toFixed(1)}%
                    </span>

                </div>

                <p>
                    $${formatMoney(
                        totals[
                            category
                        ]
                    )}/month
                </p>
            `;


            container.appendChild(
                row
            );
        }
    );
}


// --------------------------------
// PIE CHART
// --------------------------------

function createCategoryChart(
    categoryTotals
) {

    const canvas =
        document.getElementById(
            "category-chart"
        );


    if (!canvas) {
        return;
    }


    const categories =
        Object.keys(
            categoryTotals
        );


    const amounts =
        Object.values(
            categoryTotals
        );


    if (categoryChart) {

        categoryChart.destroy();

        categoryChart =
            null;
    }


    if (categories.length === 0) {
        return;
    }


    categoryChart =
        new Chart(
            canvas,
            {
                type:
                    "pie",

                data: {

                    labels:
                        categories,

                    datasets: [
                        {
                            data:
                                amounts
                        }
                    ]
                },

                options: {

                    responsive:
                        true,

                    maintainAspectRatio:
                        false,

                    plugins: {

                        legend: {

                            position:
                                "bottom"
                        }
                    }
                }
            }
        );
}


// --------------------------------
// SAVINGS CARD
// --------------------------------

function updateSavingsCard(
    categoryTotals
) {

    const card =
        document.getElementById(
            "savings-card"
        );


    const categories =
        Object.keys(
            categoryTotals
        );


    if (categories.length === 0) {

        card.innerHTML = `

            <p class="eyebrow">
                SAVINGS OPPORTUNITY
            </p>

            <h3>
                Your savings opportunities
                will appear here.
            </h3>

            <p>
                Add recurring expenses so Adisade
                can begin analysing where your
                money is going.
            </p>
        `;

        return;
    }


    let largestCategory =
        categories[0];


    categories.forEach(
        function (
            category
        ) {

            if (
                categoryTotals[
                    category
                ] >
                categoryTotals[
                    largestCategory
                ]
            ) {

                largestCategory =
                    category;
            }
        }
    );


    const amount =
        categoryTotals[
            largestCategory
        ];


    card.innerHTML = `

        <p class="eyebrow">
            SAVINGS OPPORTUNITY
        </p>

        <h3>
            A good place to review is

            <span>
                ${largestCategory}
            </span>.
        </h3>

        <p>
            You currently spend approximately

            $${formatMoney(
                amount
            )}

            per month in this category.

            Reviewing the expenses inside it
            may reveal opportunities to reduce
            recurring costs.
        </p>
    `;
}


// --------------------------------
// AI ANALYSIS
// --------------------------------

generateAIButton.addEventListener(
    "click",
    async function () {

        generateAIButton.disabled =
            true;

        generateAIButton.textContent =
            "Analysing...";

        aiLoading.classList.remove(
            "hidden"
        );

        aiResult.innerHTML =
            "";


        try {

            const response =
                await fetch(
                    "/ai-analysis",
                    {
                        method:
                            "POST"
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "AI analysis failed"
                );
            }


            const data =
                await response.json();


            aiResult.textContent =
                data.recommendation;

        } catch (error) {

            console.error(
                error
            );


            aiResult.textContent =
                "Unable to generate analysis right now.";

        } finally {

            aiLoading.classList.add(
                "hidden"
            );


            generateAIButton.disabled =
                false;


            generateAIButton.textContent =
                "Generate AI Analysis";
        }
    }
);