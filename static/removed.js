const restore_button = document.querySelectorAll(".restore-button")
const job_box = document.querySelectorAll(".jobs-display")

restore_button.forEach((button,index) => {
    button.addEventListener("click", () => changeJob(index, 0))
})