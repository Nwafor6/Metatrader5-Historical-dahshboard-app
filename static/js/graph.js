$(document).ready(() => {
  let intervalId;
  let requestId;
  let chart1;
  let chart2;
  console.log("graphjs");

  const submitForm = () => {
    let login = $("#login").val();
    // AJAX request
    $(".ajaxResponse").html("");
    $.ajax({
      type: "post",
      url: "https://tradeft9ja.pythonanywhere.com/account/",
      data: {
        login: $("#login").val(),
      },
      success: function (resp) {
        $(".canvas_holder").html("");
        console.log($("#login").val(), login, "compare");
        console.log(resp, "ajax");
        // localStorage.removeItem(login)
        // localStorage.setItem(login, JSON.stringify(resp))
        getData(resp);
      },
      error: function (err) {
        console.log(err);
        // getData(login)
        $(".ajaxResponse").html(`
            <div class="alert alert-danger" role="alert">
            Failed to fetch live data due to network error. Retrying...
            </div>
            `);
        if (err.status === 500) {
          $(".canvas_holder").html(`<div class="alert alert-danger" role="alert">
            Failed to fetch live data due to network error. Retrying...
            </div>`);
        }
      },
    });

    console.log("function called in data.js");
  };

  $("form").submit((e) => {
    e.preventDefault();
    clearInterval(requestId);

    submitForm(); // Call the submitForm function to handle the form submission

    // Schedule next AJAX request after 30 seconds
    requestId = setInterval(submitForm, 60000);
  });
      // function to to render cheched data from localhost
     function getData (resp) {
        
        if (chart1) {
            chart1.destroy();
            chart2.destroy();
          }
        $(".canvas_holder").html("");
        let account = resp.details;
        console.log(account);
        let timestamp = [];
        let equity = [];
        let balance = [];
        account.forEach((e) => {
          let js_datetime = new Date(`${e.watch_time}`);
          js_datetime = js_datetime.toString();
          timestamp.push(js_datetime.slice(4, 24));
          equity.push(e.equity);
          balance.push(e.balance);
          $("#equity").text(`${e.equity}`);
          $("#balance").text(`${e.balance}`);
        });
    
        // Populate Account1
        function loadAccount() {
          const data = {
            labels: timestamp.map((e) => e),
            datasets: [
              {
                label: "Equity",
                data: equity.map((e) => e),
                borderColor: "red",
                fill: false,
              },
              {
                label: "Balance",
                data: balance.map((e) => e),
                borderColor: "blue",
                fill: false,
              },
            ],
          };
    
          const config = {
            type: "line",
            data,
            options: {
              scales: {
                x: {
                  title: {
                    display: true,
                    text: "Time",
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "Equity and Balance",
                  },
                },
              },
            },
          };
    
          // Create new chart
          chart1 = new Chart(
            document.getElementById("chart_acc").getContext("2d"),
            config
          );
          chart2 = new Chart(
            document.getElementById("chart_acc_largeview").getContext("2d"),
            config
          );
        }
    
        loadAccount();
        console.log("Function called in graph")
      }
})

