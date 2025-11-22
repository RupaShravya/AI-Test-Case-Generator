let lastResult = []; // Store last generated test cases for CSV

async function generate() {
    const requirement = document.getElementById("req").value;
    if (!requirement) {
        alert("Please enter a requirement.");
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/generate-testcases", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ requirement })
        });

        const data = await res.json();
        lastResult = data.result;
        document.getElementById("output").textContent = JSON.stringify(data.result, null, 2);

    } catch (err) {
        console.error("ERROR:", err);
        document.getElementById("output").textContent = "Error: " + err;
    }
}

function downloadCSV() {
    if (!lastResult.length) {
        alert("Generate test cases first!");
        return;
    }

    let csv = "Type,Description,Expected Result,Steps\n";
    lastResult.forEach(tc => {
        const steps = tc.steps.join(" | "); // separate steps with pipe
        csv += `"${tc.type}","${tc.description}","${tc.expected_result}","${steps}"\n`;
    });

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "testcases.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
