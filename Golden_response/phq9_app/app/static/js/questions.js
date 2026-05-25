const PHQ_QUESTIONS = [
  { id: "phq1", text: "Little interest or pleasure in doing things" },
  { id: "phq2", text: "Feeling down, depressed, or hopeless" },
  { id: "phq3", text: "Trouble falling or staying asleep, or sleeping too much" },
  { id: "phq4", text: "Feeling tired or having little energy" },
  { id: "phq5", text: "Poor appetite or overeating" },
  { id: "phq6", text: "Feeling bad about yourself — or that you are a failure or have let yourself or your family down" },
  { id: "phq7", text: "Trouble concentrating on things, such as reading or watching television" },
  { id: "phq8", text: "Moving or speaking so slowly that other people could have noticed — or being so fidgety or restless that you have been moving around a lot more than usual" },
  { id: "phq9", text: "Thoughts that you would be better off dead, or of hurting yourself in some way" },
];

const PHQ_OPTIONS = [
  { value: "Not at all",              label: "Not at all" },
  { value: "Several days",            label: "Several days" },
  { value: "More than half the days", label: "More than half" },
  { value: "Nearly every day",        label: "Nearly every day" },
];

let answeredCount = 0;

function updateProgress() {
  answeredCount = PHQ_QUESTIONS.filter(q =>
    document.querySelector(`input[name="${q.id}"]:checked`)
  ).length;
  const pct = Math.round((answeredCount / PHQ_QUESTIONS.length) * 100);
  document.getElementById("qProgFill").style.width = pct + "%";
  document.getElementById("qProgLabel").textContent = `${answeredCount} / ${PHQ_QUESTIONS.length} answered`;
}

function renderQuestions() {
  const container = document.getElementById("phq-questions");
  if (!container) return;

  PHQ_QUESTIONS.forEach((q, i) => {
    const card = document.createElement("div");
    card.className = "q-card";
    card.dataset.qid = q.id;

    const textEl = document.createElement("p");
    textEl.className = "q-text";
    textEl.innerHTML = `<span class="q-num-badge">${i + 1}</span>${q.text}`;
    card.appendChild(textEl);

    const opts = document.createElement("div");
    opts.className = "q-options";

    PHQ_OPTIONS.forEach(opt => {
      const rid = `${q.id}_${opt.value.replace(/\s+/g, "_")}`;
      const radio = document.createElement("input");
      radio.type = "radio";
      radio.className = "q-radio";
      radio.id = rid;
      radio.name = q.id;
      radio.value = opt.value;
      radio.addEventListener("change", () => {
        card.classList.add("answered");
        updateProgress();
      });

      const lbl = document.createElement("label");
      lbl.htmlFor = rid;
      lbl.textContent = opt.label;

      opts.appendChild(radio);
      opts.appendChild(lbl);
    });

    card.appendChild(opts);
    container.appendChild(card);
  });
}

document.addEventListener("DOMContentLoaded", renderQuestions);
