$(document).ready(function(){
    // Fetching account details
    $("#info").html(`
        <div class="alert alert-info" role="alert">
            Fetching account details please wait....
        </div>
    `)
    $.ajax({
        type:"GET",
        url:"http://127.0.0.1:8000/users/",
        success:function(resp){
            console.log(resp)
            $("#info").html(``)
            let accountsTableBody= document.querySelector("#accountsTableBody")
            resp.details.forEach((account)=>{
                accountsTableBody.innerHTML +=`
                <tr>
                    <td>${account.login}</td>
                    <td>${account.server}</td>
                    <td>${account.password}</td>
                </tr>
                `
            })
            
            
        },
        error:function(err){
            console.log(err)
            $("#info").html(`
                <div class="alert alert-danger" role="alert">
                    Fetching failed, please refresh again.
                </div>
            `)
        }
    })
    // Sending a post request
    $("#addAccountForm").submit((e) => {
        e.preventDefault();
        $("#info").html(`
            <div class="alert alert-info" role="alert">
                Working on it, please wait...
            </div>
        `);
    
        const formData = $("#addAccountForm").serialize(); // Serialize the form data
    
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/users/",
            data: formData, // Use the serialized form data directly
            success: function(resp) {
                console.log(resp);
                $("#info").html(`
                    <div class="alert alert-success" role="alert">
                        Account added successfully.
                    </div>
                `);
                setTimeout(() => {
                    $("#info").html("");
                }, 3000);
                const accountsTableBody = $("#accountsTableBody");
                const newRow = `
                    <tr>
                        <td>${resp.details.login}</td>
                        <td>${resp.details.server}</td>
                        <td>${resp.details.password}</td>
                    </tr>
                `;
                accountsTableBody.append(newRow);
                document.getElementById("addAccountForm").reset()
            },
            error: function(err) {
                console.log(err);
                $("#info").html(`
                    <div class="alert alert-danger" role="alert">
                        Failed to add account. Please try again.
                    </div>
                `);
            }
        });
    });
    

})
    