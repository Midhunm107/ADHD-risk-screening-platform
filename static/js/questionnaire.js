// Questionnaire: one question at a time, client-side only.
//
// Items are the ASRS-v1.1 Part A screener (6 questions) -- the instrument
// CLAUDE.md identifies as the one this website's questionnaire should use
// (distinct from HYPERAKTIV's 18-item ASRS column). No submission endpoint
// exists yet, so "Finish" just reveals a completion note instead of
// posting anywhere.

document.addEventListener("DOMContentLoaded", function () {
  var QUESTIONS = [
    "How often do you have trouble wrapping up the final details of a project, once the challenging parts have been done?",
    "How often do you have difficulty getting things in order when you have to do a task that requires organization?",
    "How often do you have problems remembering appointments or obligations?",
    "When you have a task that requires a lot of thought, how often do you avoid or delay getting started?",
    "How often do you fidget or squirm with your hands or feet when you have to sit for a long time?",
    "How often do you feel overly active and compelled to do things, like you were driven by a motor?"
  ];

  var OPTIONS = ["Never", "Rarely", "Sometimes", "Often", "Very Often"];

  var answers = new Array(QUESTIONS.length).fill(null);
  var current = 0;

  var questionMeta = document.getElementById("question-meta");
  var progressPercent = document.getElementById("progress-percent");
  var progressFill = document.getElementById("progress-fill");
  var questionText = document.getElementById("question-text");
  var optionsList = document.getElementById("options-list");
  var btnPrevious = document.getElementById("btn-previous");
  var btnNext = document.getElementById("btn-next");
  var questionCard = document.getElementById("question-card");
  var completionPanel = document.getElementById("completion-panel");

  function render() {
    var n = current + 1;
    var percent = Math.round((n / QUESTIONS.length) * 100);

    questionMeta.textContent = "Question " + n + " of " + QUESTIONS.length;
    progressPercent.textContent = percent + "%";
    progressFill.style.width = percent + "%";
    questionText.textContent = QUESTIONS[current];

    optionsList.innerHTML = "";
    OPTIONS.forEach(function (label, i) {
      var id = "q" + current + "-opt" + i;

      var wrapper = document.createElement("label");
      wrapper.className = "radio-option";
      wrapper.setAttribute("for", id);

      var input = document.createElement("input");
      input.type = "radio";
      input.name = "question-" + current;
      input.id = id;
      input.value = label;
      input.checked = answers[current] === label;
      input.addEventListener("change", function () {
        answers[current] = label;
        btnNext.disabled = false;
      });

      wrapper.appendChild(input);
      wrapper.appendChild(document.createTextNode(label));
      optionsList.appendChild(wrapper);
    });

    btnPrevious.disabled = current === 0;
    btnNext.disabled = answers[current] === null;
    btnNext.textContent = current === QUESTIONS.length - 1 ? "Finish" : "Next →";
  }

  btnPrevious.addEventListener("click", function () {
    if (current > 0) {
      current -= 1;
      render();
    }
  });

  btnNext.addEventListener("click", function () {
    if (answers[current] === null) {
      return;
    }
    if (current < QUESTIONS.length - 1) {
      current += 1;
      render();
    } else {
      questionCard.hidden = true;
      completionPanel.hidden = false;
    }
  });

  render();
});
