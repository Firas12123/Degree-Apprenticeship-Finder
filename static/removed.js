const restore_button = document.querySelectorAll(".restore-button")
const job_box = document.querySelectorAll(".jobs-display")
const no_jobs = document.getElementById("no-jobs")

restore_button.forEach((button,index) => {
    button.addEventListener("click", () => changeJob(index, 0))
})
if (job_box.length > 0){
    no_jobs.classList.add("active")
}
