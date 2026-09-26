const add_button = document.getElementById("plus-button");
const minus_button = document.getElementById("minus-button");
const tick_box = document.querySelector(".tick-box")
const tick_display = document.querySelectorAll(".tick")
let applied_for = document.getElementById("applied-counter")
let count = 3;

applied_for.textContent = "Total DA's applied for : "+ count;
function changeCount(choice){
    if (choice === "-"){
        if (count > 0){
            count--;
        }
    }
    else if (choice === "+") {
        count++;
    }
    applied_for.textContent = "Total DA's applied for : "+ count;
}

function appliedCheck(item){
    tick_display[item].classList.add("active")
}

add_button.addEventListener("click", () => changeCount("+"));
minus_button.addEventListener("click", () => changeCount("-"));
tick_box.addEventListener("click", appliedCheck(tick_box.index()))

