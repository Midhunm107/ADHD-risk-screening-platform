// Consent page: keep "Continue" disabled until the checkbox is checked,
// then move on to the questionnaire.

document.addEventListener("DOMContentLoaded", function () {
  var checkbox = document.getElementById("consent-checkbox");
  var continueBtn = document.getElementById("consent-continue");
  var form = document.getElementById("consent-form");

  checkbox.addEventListener("change", function () {
    continueBtn.disabled = !checkbox.checked;
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!checkbox.checked) {
      return;
    }
    window.location.href = continueBtn.dataset.next;
  });
});
