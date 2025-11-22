async function generate() {
    const requirement = document.getElementById("req").value.trim();

    if (!requirement) {
        alert("Please enter a requirement!");
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/generate-testcases", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ requirement })
        });

        const data = await res.json();

        const outputDiv = document.getElementById("output");
        outputDiv.innerHTML = ""; // Clear previous output

        data.result.forEach(tc => {
            const tcDiv = document.createElement("div");
            tcDiv.className = "test-case";

            let html = `<strong>Test Case ${tc.test_case}:</strong> ${tc.description}<br>`;
            html += `<strong>Expected Result:</strong> ${tc.expected_result}<br>`;
            html += `<strong>Steps:</strong><ol>`;
            tc.steps.forEach(step => { html += `<li>${step}</li>`; });
            html += `</ol>`;

            tcDiv.innerHTML = html;
            outputDiv.appendChild(tcDiv);
        });

    } catch (err) {
        console.error("Error fetching data:", err);
        document.getElementById("output").textContent = "Error fetching data from backend";
    }
}
