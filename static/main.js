const add_button = document.getElementById("plus-button");
const minus_button = document.getElementById("minus-button");
const tick_box = document.querySelectorAll  (".tick-box");
const tick_display = document.querySelectorAll(".tick");
const job_box = document.querySelectorAll(".jobs-display")
let applied_for = document.getElementById("applied-counter");
let amount = Number(localStorage.getItem("counter"));
const apply_button = document.querySelectorAll(".apply-button")
const cancel_button = document.querySelectorAll(".cancel-button")
const confirm_choice = document.querySelectorAll(".confirm")
const cancel_b = document.querySelectorAll(".cancel-b")
const overlays = document.querySelectorAll(".overlay")
const submit_job = document.getElementById("submit-job")
const clear_jobs = document.getElementById("clear-search")
const jobs_list = document.getElementById("jobs")
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

function confirmChoice(index){
    confirm_choice[index].classList.add("active")
    overlays[index].classList.add("active")
}

tick_box.forEach((box, index) =>{
    box.addEventListener("click", () => appliedFor(index));
})

cancel_button.forEach((box, index) =>{
    box.addEventListener("click", () => confirmChoice(index))
})

cancel_b.forEach((canceler, index) => {
    const overlay = overlays[index]
    const confirm = confirm_choice[index]
    const removeOverlay = () => {
        overlay.classList.remove("active")
        confirm.classList.remove("active")
    }
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay){
            removeOverlay();
        }
    })
    canceler.addEventListener("click", removeOverlay);
})
const job_title = document.getElementById("job-search");
job_title.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault()
        searchJobs();
    }
});

function searchJobs(task){
    let all_jobs = JSON.parse(localStorage.getItem("jobs")) || []
    all_jobs.push(job_title.value)
    localStorage.setItem("jobs", JSON.stringify(all_jobs))
    fetch("/jobs",{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            job_title: all_jobs,
            delete: task
        })
    })
    .then(response =>{
        if(response.status === 201){
            localStorage.setItem("jobs", "[]")
            location.reload()
        }
        else{
            location.reload()    // refreshes only when ready
        }
    })
}
function displayJobs() {
    const all_jobs= JSON.parse(localStorage.getItem("jobs")) || []
    all_jobs.forEach(job => {
        const li = document.createElement("li");
        li.textContent = job;
        jobs_list.appendChild(li);
    })
}


submit_job.addEventListener("click", () => searchJobs(""));
clear_jobs.addEventListener("click", () => searchJobs("delete"));
add_button.addEventListener("click", () => changeCount("+"));
minus_button.addEventListener("click", () => changeCount("-"));
displayJobs();
