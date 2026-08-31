// Consent page: keep "Continue" disabled until the checkbox is checked.
// The questionnaire route doesn't exist yet, so submitting just reveals a
// note instead of navigating anywhere.

document.addEventListener("DOMContentLoaded", function () {
  var checkbox = document.getElementById("consent-checkbox");
  var continueBtn = document.getElementById("consent-continue");
  var form = document.getElementById("consent-form");
  var nextNote = document.getElementById("consent-next-note");

  checkbox.addEventListener("change", function () {
    continueBtn.disabled = !checkbox.checked;
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    nextNote.hidden = false;
  });
});
