$(document).ready(() => {

    
    console.log("datajs")
    $("form").submit((e) => {
      console.log("Hello my people from index");
      e.preventDefault();
      $(".canvas_holder").html(`
        <div class="text-center">
          <div class="spinner-border" style="width: 3rem; height: 3rem;" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      `);
      // let login=$("#login").val()
      // if(!localStorage.getItem(login)){
      //   localStorage.setItesm(login,"")
      //   console.log(localStorage.getItem(login))
    // }
      // setInterval(() => {
      //   // AJAX request
      //   $.ajax({
      //     type: "post",
      //     url: "http://127.0.0.1:8000/account/",
      //     data: {
      //       login: $("#login").val(),
      //     },
      //     success: function (resp) {
      //       $(".canvas_holder").html(``)
      //       localStorage.removeItem(login)
      //       localStorage.setItem(login, JSON.stringify(resp))
      //       console.log(resp)
      //     },
      //     error: function (err) {
      //       console.log(err);
      //       if(err.status===500){
      //           alert("Network error, can't tech data")
      //       }
      //     },
      //   });
      // }, 60000); // End interval
      // console.log("function called in data.js")
    });
  });

