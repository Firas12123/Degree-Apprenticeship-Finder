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
            if (response.status === 200){
            location.reload();
            }
        })
    location.reload()
}