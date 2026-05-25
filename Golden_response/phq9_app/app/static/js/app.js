/* ── State ── */
let lastPayload = null;
let currentStep = 1;

/* ── DOM ── */
const phqForm       = document.getElementById("phqForm");
const step1         = document.getElementById("step1");
const step2         = document.getElementById("step2");
const resultsSection= document.getElementById("resultsSection");
const errorBanner   = document.getElementById("errorBanner");
const submitBtn     = document.getElementById("submitBtn");

/* ── Progress steps ── */
function setStep(n) {
  currentStep = n;
  document.querySelectorAll(".prog-step").forEach(el => {
    const s = parseInt(el.dataset.step);
    el.classList.toggle("active", s === n);
    el.classList.toggle("done",   s < n);
  });
  document.querySelectorAll(".prog-line").forEach((el, i) => {
    el.classList.toggle("done", i < n - 1);
  });
}

/* ── Toggle button groups ── */
function initToggleGroup(containerId, hiddenId) {
  document.getElementById(containerId).addEventListener("click", e => {
    const btn = e.target.closest(".toggle-btn");
    if (!btn) return;
    document.querySelectorAll(`#${containerId} .toggle-btn`).forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    document.getElementById(hiddenId).value = btn.dataset.val;
  });
}
function initScaleGroup(containerId, hiddenId) {
  document.getElementById(containerId).addEventListener("click", e => {
    const btn = e.target.closest(".scale-btn");
    if (!btn) return;
    document.querySelectorAll(`#${containerId} .scale-btn`).forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    document.getElementById(hiddenId).value = btn.dataset.val;
  });
}

initToggleGroup("genderToggle", "gender");
initScaleGroup("sleepToggle",   "sleep_quality");
initScaleGroup("studyToggle",   "study_pressure");
initScaleGroup("finToggle",     "financial_pressure");

/* ── Step navigation ── */
document.getElementById("toStep2Btn").addEventListener("click", () => {
  const age    = parseInt(document.getElementById("age").value, 10);
  const gender = document.getElementById("gender").value;
  const sleep  = document.getElementById("sleep_quality").value;
  const study  = document.getElementById("study_pressure").value;
  const fin    = document.getElementById("financial_pressure").value;

  const errs = [];
  if (!age || age < 10 || age > 100) errs.push("Please enter a valid age (10–100).");
  if (!gender) errs.push("Please select your gender.");
  if (!sleep)  errs.push("Please select your sleep quality.");
  if (!study)  errs.push("Please select your study/work pressure.");
  if (!fin)    errs.push("Please select your financial pressure level.");

  if (errs.length) { showError(errs[0]); return; }
  hideError();
  step1.classList.add("hidden");
  step2.classList.remove("hidden");
  setStep(2);
  window.scrollTo({ top: 0, behavior: "smooth" });
});

document.getElementById("toStep1Btn").addEventListener("click", () => {
  step2.classList.add("hidden");
  step1.classList.remove("hidden");
  setStep(1);
  window.scrollTo({ top: 0, behavior: "smooth" });
});

/* ── Error helpers ── */
function showError(msg) {
  errorBanner.textContent = msg;
  errorBanner.classList.remove("hidden");
  errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
}
function hideError() { errorBanner.classList.add("hidden"); }

/* ── Payload ── */
function collectPayload() {
  const d = {
    age:               parseInt(document.getElementById("age").value, 10),
    gender:            document.getElementById("gender").value,
    sleep_quality:     document.getElementById("sleep_quality").value,
    study_pressure:    document.getElementById("study_pressure").value,
    financial_pressure:document.getElementById("financial_pressure").value,
  };
  for (let i = 1; i <= 9; i++) {
    const checked = document.querySelector(`input[name="phq${i}"]:checked`);
    d[`phq${i}`] = checked ? checked.value : null;
  }
  return d;
}

/* ── Form submit ── */
phqForm.addEventListener("submit", async e => {
  e.preventDefault();
  hideError();
  const payload = collectPayload();

  for (let i = 1; i <= 9; i++) {
    if (!payload[`phq${i}`]) {
      showError(`Please answer question ${i}.`);
      return;
    }
  }

  lastPayload = payload;
  submitBtn.disabled = true;
  submitBtn.classList.add("loading");

  try {
    const res  = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) { showError(data.error || "Prediction failed."); return; }
    renderResults(data);
  } catch {
    showError("Network error. Please check your connection and try again.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.classList.remove("loading");
  }
});

/* ── Severity helpers ── */
const SEV_MAP = {
  "Minimal":           { cls: "sev-0", icon: "○" },
  "Mild":              { cls: "sev-1", icon: "◔" },
  "Moderate":          { cls: "sev-2", icon: "◑" },
  "Moderately Severe": { cls: "sev-3", icon: "◕" },
  "Severe":            { cls: "sev-4", icon: "●" },
};

/* ── Render results ── */
function renderResults(result) {
  const { phq_score, severity, confidence, explanation, suggestions } = result;
  const sev = SEV_MAP[severity] || { cls: "sev-2", icon: "◑" };

  /* Ring */
  const ring   = document.getElementById("ringFill");
  const circ   = 2 * Math.PI * 50;
  const filled = (phq_score / 27) * circ;
  ring.setAttribute("stroke-dasharray", `${filled.toFixed(1)} ${circ.toFixed(1)}`);
  ring.className = `ring-fill ${sev.cls}`;
  document.getElementById("scoreNum").textContent = phq_score.toFixed(1);

  /* Severity */
  const sevIcon = document.getElementById("sevIcon");
  const sevText = document.getElementById("severityText");
  sevIcon.textContent = sev.icon;
  sevIcon.className   = `sev-icon ${sev.cls}`;
  sevText.textContent = severity;
  sevText.className   = `sev-text ${sev.cls}`;

  /* Confidence arc (half-circle arc length ≈ 126) */
  const arc     = document.getElementById("arcFill");
  const arcLen  = 126;
  const arcFill = confidence * arcLen;
  arc.setAttribute("stroke-dasharray", `${arcFill.toFixed(1)} ${arcLen.toFixed(1)}`);
  arc.className = `arc-fill ${sev.cls}`;
  document.getElementById("confNum").textContent = Math.round(confidence * 100) + "%";

  /* Explanation list */
  const exList = document.getElementById("explanationList");
  exList.innerHTML = "";
  (explanation || []).forEach((item, i) => {
    const li = document.createElement("li");
    li.className = `factor-item factor-${item.direction === "increased" ? "up" : "down"}`;
    li.style.animationDelay = `${i * 0.07}s`;
    li.innerHTML = `
      <span class="factor-dir">${item.direction === "increased" ? "↑" : "↓"}</span>
      <span>${item.explanation}</span>
    `;
    exList.appendChild(li);
  });

  /* Suggestions */
  const sugList = document.getElementById("suggestionList");
  sugList.innerHTML = "";
  (suggestions || []).forEach((s, i) => {
    const li = document.createElement("li");
    li.className = "sug-item";
    li.style.animationDelay = `${i * 0.06}s`;
    li.innerHTML = `<span class="sug-bullet" aria-hidden="true"></span><span>${s}</span>`;
    sugList.appendChild(li);
  });

  /* Show results */
  step2.classList.add("hidden");
  phqForm.classList.add("hidden");
  resultsSection.classList.remove("hidden");
  setStep(3);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ── PDF download ── */
document.getElementById("downloadBtn").addEventListener("click", async () => {
  if (!lastPayload) return;
  const btn = document.getElementById("downloadBtn");
  btn.textContent = "Generating…";
  btn.disabled = true;
  try {
    const res  = await fetch("/report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastPayload),
    });
    if (!res.ok) { showError("Could not generate the report. Please try again."); return; }
    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href = url; a.download = "phq9_wellness_report.pdf";
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  } catch { showError("Download failed. Please try again."); }
  finally {
    btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M8 2v8M5 7l3 3 3-3M3 13h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg> Download PDF report`;
    btn.disabled = false;
  }
});

/* ── Retake ── */
document.getElementById("retakeBtn").addEventListener("click", () => {
  phqForm.reset();
  phqForm.classList.remove("hidden");
  document.querySelectorAll(".q-card").forEach(c => c.classList.remove("answered"));
  document.querySelectorAll(".toggle-btn, .scale-btn").forEach(b => b.classList.remove("selected"));
  document.querySelectorAll("input[type=hidden]").forEach(i => i.value = "");
  document.getElementById("qProgFill").style.width = "0%";
  document.getElementById("qProgLabel").textContent = "0 / 9 answered";
  resultsSection.classList.add("hidden");
  step1.classList.remove("hidden");
  step2.classList.add("hidden");
  hideError();
  lastPayload = null;
  setStep(1);
  window.scrollTo({ top: 0, behavior: "smooth" });
});
