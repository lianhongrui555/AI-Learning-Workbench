async function apiJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `请求失败：HTTP ${response.status}`);
  return data;
}

function appendTutorLine(container, role, text) {
  if (!container) return;
  const line = document.createElement("div");
  line.className = `tutor-line ${role}`;
  const label = document.createElement("span");
  label.textContent = role === "user" ? "you@local:~$" : "tutor@local:~$";
  const body = document.createElement("p");
  body.textContent = text;
  line.append(label, body);
  container.appendChild(line);
  container.scrollTop = container.scrollHeight;
}

async function sendTutorMessage(lessonId, message, messagesElement, statusElement, conversationId = "") {
  appendTutorLine(messagesElement, "user", message);
  statusElement.textContent = "助教正在思考……";
  const data = await apiJson("/api/tutor", {
    method: "POST",
    body: JSON.stringify({ lesson_id: lessonId, message, conversation_id: conversationId }),
  });
  appendTutorLine(messagesElement, "assistant", data.answer);
  statusElement.textContent = "回答完成。";
  return data;
}

document.addEventListener("DOMContentLoaded", () => {
  const lessonPage = document.querySelector(".lesson-page");
  if (lessonPage) {
    const lessonId = lessonPage.dataset.lessonId;
    const completeButton = document.getElementById("lesson-complete");
    const progressLabel = document.getElementById("lesson-progress-label");

    if (completeButton) {
      completeButton.addEventListener("click", async () => {
        const completed = completeButton.dataset.completed !== "1";
        try {
          await apiJson(`/api/progress/${lessonId}`, { method: "POST", body: JSON.stringify({ completed }) });
          completeButton.dataset.completed = completed ? "1" : "0";
          completeButton.textContent = completed ? "标记未完成" : "标记完成";
          if (progressLabel) progressLabel.textContent = completed ? "已完成" : "未完成";
        } catch (error) {
          alert(error.message);
        }
      });
    }

    const saveNoteButton = document.getElementById("save-note");
    if (saveNoteButton) {
      saveNoteButton.addEventListener("click", async () => {
        const note = document.getElementById("note-content").value;
        const status = document.getElementById("note-status");
        status.textContent = "保存中……";
        try {
          await apiJson(`/api/notes/${lessonId}`, { method: "PUT", body: JSON.stringify({ content: note }) });
          status.textContent = "笔记已保存到本地。";
        } catch (error) {
          status.textContent = `保存失败：${error.message}`;
        }
      });
    }

    const quizForm = document.getElementById("quiz-form");
    if (quizForm) {
      quizForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const answers = {};
        new FormData(quizForm).forEach((value, key) => { answers[key] = value; });
        const resultBox = document.getElementById("quiz-result");
        resultBox.className = "result-box";
        try {
          const data = await apiJson(`/api/quiz/${lessonId}/submit`, { method: "POST", body: JSON.stringify({ answers }) });
          resultBox.classList.add(data.score >= 60 ? "success" : "error");
          resultBox.textContent = `得分 ${data.score} 分（${data.correct}/${data.total}）。${data.details.map((item) => `${item.id}: ${item.correct ? "正确" : "需复习"}`).join("；")}`;
        } catch (error) {
          resultBox.classList.add("error");
          resultBox.textContent = error.message;
        }
      });
    }

    const tutorForm = document.getElementById("tutor-form");
    if (tutorForm) {
      let conversationId = "";
      tutorForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const input = document.getElementById("tutor-input");
        const status = document.getElementById("tutor-status");
        const messages = document.getElementById("tutor-messages");
        const message = input.value.trim();
        if (!message) return;
        input.value = "";
        try {
          const data = await sendTutorMessage(lessonId, message, messages, status, conversationId);
          conversationId = data.conversation_id || conversationId;
        } catch (error) {
          status.textContent = `请求失败：${error.message}`;
        }
      });
    }
  }

  document.querySelectorAll(".project-card").forEach((card) => {
    const button = card.querySelector(".project-toggle");
    if (!button) return;
    button.addEventListener("click", async () => {
      const projectId = card.dataset.projectId;
      const completed = button.dataset.completed !== "1";
      try {
        await apiJson(`/api/projects/${projectId}/progress`, { method: "POST", body: JSON.stringify({ completed }) });
        button.dataset.completed = completed ? "1" : "0";
        button.textContent = completed ? "标记未完成" : "标记完成";
        card.querySelector(".status-pill").textContent = completed ? "DONE" : "OPEN";
      } catch (error) {
        alert(error.message);
      }
    });
  });

  const tutorPage = document.querySelector("[data-tutor-page]");
  if (tutorPage) {
    const select = document.getElementById("tutor-lesson-select");
    select.addEventListener("change", () => { window.location.href = `/tutor?lesson_id=${encodeURIComponent(select.value)}`; });
    const form = document.getElementById("tutor-form");
    const messages = document.getElementById("tutor-messages");
    const status = document.getElementById("tutor-status");
    let conversationId = "";
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const input = document.getElementById("tutor-input");
      const message = input.value.trim();
      if (!message) return;
      input.value = "";
      try {
        const data = await sendTutorMessage(select.value, message, messages, status, conversationId);
        conversationId = data.conversation_id || conversationId;
      } catch (error) {
        status.textContent = `请求失败：${error.message}`;
      }
    });
  }
});