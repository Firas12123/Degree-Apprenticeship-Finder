const add_button = document.getElementById("plus-button");
const minus_button = document.getElementById("minus-button");
const tick_box = document.querySelectorAll  (".tick-box");
const tick_display = document.querySelectorAll(".tick");
const job_box = document.querySelectorAll(".jobs-display")
let applied_for = document.getElementById("applied-counter");
let amount = Number(localStorage.getItem("counter"));
const apply_button = document.querySelectorAll(".apply-button")
let total_applied = 0

job_box.forEach((box, index) => {
    if (Number(job_box[index].dataset.applied) === 1) {
        tick_display[index].classList.add("active")
        total_applied++
        apply_button[index].textContent = "Applied"
        apply_button[index].classList.add("active")
    }
})

    if (amount === null) {
        amount = 0;
    } else {
        amount = Number(amount)
    }

applied_for.textContent = "Total DA's applied for : " + amount;
function changeCount(choice) {
    if (choice === "-") {
        if (amount > total_applied) {
            amount--;
        }
    } else if (choice === "+") {
        amount++;
    }
    localStorage.setItem("counter", String(amount))
    applied_for.textContent = "Total DA's applied for : " + amount;
}

function appliedFor(index) {
    let applied = Number(job_box[index].dataset.applied)
    if (applied === 0) {
        tick_display[index].classList.add("active");
        applied = 1
        total_applied++;
        amount++
        apply_button[index].classList.add("active")
        apply_button[index].textContent = "Applied"

    } else if (applied === 1) {
        tick_display[index].classList.remove("active")
        applied = 0
        total_applied--
        amount--
        apply_button[index].classList.remove("active")
        apply_button[index].textContent = "Apply here"
    }
    job_box[index].dataset.applied = String(applied)

    let job_id = Number(job_box[index].dataset.id)
    fetch("/checked", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            applied: applied,
            job_id: job_id
        })
    });
    localStorage.setItem("counter", String(amount))
    applied_for.textContent = "Total DA's applied for : " + amount;
}

tick_box.forEach((box, index) =>{
    box.addEventListener("click", () => appliedFor(index));
})

add_button.addEventListener("click", () => changeCount("+"));
minus_button.addEventListener("click", () => changeCount("-"));

