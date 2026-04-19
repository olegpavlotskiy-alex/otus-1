/**
 * Мини-анкета: загрузка вопросов с Flask API и отправка ответов.
 * Укажите URL бэкенда (по умолчанию http://127.0.0.1:5000).
 */
const API_BASE = "http://127.0.0.1:5000";

const form = document.getElementById("survey-form");
const fieldsEl = document.getElementById("fields");
const messageEl = document.getElementById("message");
const thankYouEl = document.getElementById("thank-you");
const submitBtn = document.getElementById("submit-btn");

function showMessage(text, type) {
  messageEl.textContent = text;
  messageEl.hidden = false;
  messageEl.className = "message " + (type === "error" ? "error" : "info");
}

function hideMessage() {
  messageEl.hidden = true;
  messageEl.textContent = "";
  messageEl.className = "message";
}

function renderQuestions(questions) {
  fieldsEl.innerHTML = "";
  questions.forEach((q) => {
    const div = document.createElement("div");
    div.className = "field";
    const label = document.createElement("label");
    label.htmlFor = "q-" + q.id;
    label.textContent = q.text;
    const input = document.createElement("input");
    input.type = "text";
    input.id = "q-" + q.id;
    input.name = q.id;
    input.required = true;
    input.autocomplete = "off";
    div.appendChild(label);
    div.appendChild(input);
    fieldsEl.appendChild(div);
  });
}

function collectAnswers(questions) {
  return questions.map((q) => {
    const input = document.getElementById("q-" + q.id);
    return {
      question_id: q.id,
      text: input ? input.value : "",
    };
  });
}

async function loadQuestions() {
  hideMessage();
  submitBtn.disabled = true;
  showMessage("Загрузка вопросов…", "info");
  try {
    const res = await fetch(API_BASE + "/questions");
    if (!res.ok) {
      throw new Error("Сервер вернул код " + res.status);
    }
    const data = await res.json();
    if (!data.questions || !Array.isArray(data.questions)) {
      throw new Error("Неверный формат ответа API");
    }
    hideMessage();
    renderQuestions(data.questions);
    form.dataset.questions = JSON.stringify(data.questions);
    submitBtn.disabled = false;
  } catch (e) {
    showMessage(
      "Не удалось загрузить вопросы. Убедитесь, что backend запущен (см. README). " +
        (e.message || ""),
      "error"
    );
    fieldsEl.innerHTML = "";
  }
}

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  hideMessage();
  const raw = form.dataset.questions;
  if (!raw) {
    showMessage("Вопросы ещё не загружены.", "error");
    return;
  }
  let questions;
  try {
    questions = JSON.parse(raw);
  } catch {
    showMessage("Ошибка данных формы.", "error");
    return;
  }

  const answers = collectAnswers(questions);
  submitBtn.disabled = true;
  showMessage("Отправка…", "info");

  try {
    const res = await fetch(API_BASE + "/answers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers }),
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      const msg = body.error || "Ошибка отправки (код " + res.status + ")";
      throw new Error(msg);
    }
    hideMessage();
    form.hidden = true;
    thankYouEl.hidden = false;
  } catch (e) {
    showMessage(e.message || "Ошибка сети или сервера.", "error");
    submitBtn.disabled = false;
  }
});

loadQuestions();
