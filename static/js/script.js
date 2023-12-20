document.addEventListener("DOMContentLoaded", function() {
  let id = (id) => document.getElementById(id);
  let form = id("form");
  let errorMsg = document.querySelectorAll(".error");

  form.addEventListener("submit", (e) => {
      e.preventDefault();

      // Collect data from the form
      let formData = {
          CNT_CHILDREN: Number(id("CNT_CHILDREN").value.trim()),
          AMT_INCOME_TOTAL: id("AMT_INCOME_TOTAL").value.trim(),
          AMT_CREDIT: id("AMT_CREDIT").value.trim(),
          AMT_ANNUITY: id("AMT_ANNUITY").value.trim(),
          AMT_GOODS_PRICE: id("AMT_GOODS_PRICE").value.trim(),
          REGION_POPULATION_RELATIVE: id("REGION_POPULATION_RELATIVE").value.trim(),
          DAYS_BIRTH: id("DAYS_BIRTH").value.trim(),
          DAYS_EMPLOYED: id("DAYS_EMPLOYED").value.trim(),
          DAYS_REGISTRATION: id("DAYS_REGISTRATION").value.trim(),
          DAYS_ID_PUBLISH: id("DAYS_ID_PUBLISH").value.trim(),
          FLAG_WORK_PHONE: id("FLAG_WORK_PHONE").value.trim(),
          REGION_RATING_CLIENT: id("REGION_RATING_CLIENT").value.trim(),
          HOUR_APPR_PROCESS_START: id("HOUR_APPR_PROCESS_START").value.trim()
      };

      for (const key in formData) {
        formData[key] = Number(formData[key]);
      }

      // Validate and send request
      if (validateForm(formData)) {
          sendPredictionRequest(formData);
      }
  });

  // Function to validate form data
  function validateForm(data) {
      let isValid = true;
      for (const [key, value] of Object.entries(data)) {
          if (value === "") {
              displayError(key, `${key.replace(/_/g, " ")} cannot be blank`);
              isValid = false;
          } else {
              clearError(key);
          }
      }
      return isValid;
  }

  // Function to display error
  function displayError(fieldId, message) {
      let field = id(fieldId);
      let errorDiv = field.nextElementSibling;
      errorDiv.innerHTML = message;
      field.style.border = "2px solid red";
  }

  // Function to clear error
  function clearError(fieldId) {
      let field = id(fieldId);
      let errorDiv = field.nextElementSibling;
      errorDiv.innerHTML = "";
      field.style.border = "2px solid green";
  }

//  Function to send POST request to the server
  function sendPredictionRequest(data) {
      fetch('http://localhost:5000/predict/xgboost', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
          console.log('Success:', data);
          alert(`Prediction: ${data.prediction}`);
      })
      .catch((error) => {
          console.error('Error:', error);
          alert('An error occurred while making the prediction');
      });
  }
})