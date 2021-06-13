document.addEventListener("DOMContentLoaded", () => {

    var exampleModal = document.getElementById('exampleModal')
    exampleModal.addEventListener('show.bs.modal', function (event) {

        var saveChangesButton = exampleModal.querySelector("#save_changes_button")

        saveChangesButton.onclick = () => {
            const username = document.getElementById("username_here").value
            const email = document.getElementById("email_here").value
            const address = document.getElementById("address_here").value
            const prev_email = document.getElementById("current_email").innerHTML

            document.getElementById("current_username").innerHTML = username
            document.getElementById("current_email").innerHTML = email
            document.getElementById("current_address").innerHTML = address

            // updating it in the db
            fetch('/edit_details', {
                method: 'POST',
                body: JSON.stringify({
                    email: `${email}`,
                    username: `${username}`,
                    prev_email: `${prev_email}`,
                    address: `${address}`,
                })
            })
                .then(response => response.json())
                .then(result => {
                    console.log(result)
                })

            document.querySelector('#close_modal').click()
            return true;
        }
    })
})