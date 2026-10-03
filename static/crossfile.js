function changeJob(index, choice){
    fetch("/remove",{
        method: "POST",
        headers:{
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            id: job_box[index].dataset.id,
            choice: choice,
        })
    })
        .then(response => {
            if (response.status === 200) {
                job_box[index].classList.add("active")
                const job_coord = job_box[index].getBoundingClientRect();
                const job_centerX = job_coord.left + job_coord.width / 2;
                const job_centerY = job_coord.top + job_coord.height / 2;
                if (choice === 1){
                    const bin_coord = bin_button.getBoundingClientRect();
                    const bin_centerX = bin_coord.left + bin_coord.width / 2;
                    const bin_centerY = bin_coord.top + bin_coord.height / 2;
                    const x = bin_centerX - job_centerX;
                    const y = bin_centerY - job_centerY;
                job_box[index].style.transform = `translate(${x+10}px, ${y-6}px) scale(0.01)`;
            }
                else if (choice === 0){
                    const title_button = document.getElementById("title-nav")
                    const title_coord = title_button.getBoundingClientRect();
                    const title_centerX = title_coord.left + title_coord.width / 2;
                    const title_centerY = title_coord.top + title_coord.height / 2;
                    const x = title_centerX - job_centerX
                    const y = title_centerY - job_centerY
                job_box[index].style.transform = `translate(${x+12}px, ${y+7}px) scale(0.01)`;
                }
            setTimeout(() =>{
               location.reload();
            },400);}
    });
}