const datePicker = document.getElementById("datePicker");
const hoursDiv = document.getElementById("hours");
const selectedHourInput = document.getElementById("selectedHour");

// verificare luni–vineri
function isWeekday(dateStr) {
    const date = new Date(dateStr);
    const day = date.getDay(); 
    // 0 = duminică, 6 = sâmbătă
    return day >= 1 && day <= 5;
}

datePicker.addEventListener("change", async () => {

    const date = datePicker.value;

    hoursDiv.innerHTML = "";
    selectedHourInput.value = "";

    if (!isWeekday(date)) {
        hoursDiv.innerHTML = "<p style='color:red'>Selectează doar luni - vineri</p>";
        return;
    }

    const response = await fetch("/get-hours", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ date })
    });

    const hours = await response.json();

    if (hours.length === 0) {
        hoursDiv.innerHTML = "<p>Nu mai sunt ore disponibile</p>";
        return;
    }

    hours.forEach(hour => {

        const btn = document.createElement("button");
        btn.type = "button";
        btn.innerText = hour;
        btn.classList.add("hour-btn");

        btn.addEventListener("click", () => {

            document.querySelectorAll(".hour-btn").forEach(b => {
                b.classList.remove("selected");
            });

            btn.classList.add("selected");
            selectedHourInput.value = hour;
        });

        hoursDiv.appendChild(btn);
    });
});