const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const mobileMenu = document.getElementById("mobileMenu");

const startScreen = document.getElementById("startScreen");
const chatSession = document.getElementById("chatSession");

const largeComposer = document.getElementById("largeComposer");
const largePrompt = document.getElementById("largePrompt");

const composer = document.getElementById("composer");
const prompt = document.getElementById("prompt");

const messages = document.getElementById("messages");

function openSidebar() {
  sidebar.classList.add("open");
  overlay.classList.add("show");
}

function closeSidebar() {
  sidebar.classList.remove("open");
  overlay.classList.remove("show");
}

mobileMenu.addEventListener("click", openSidebar);
overlay.addEventListener("click", closeSidebar);

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function addMessage(type, text) {

  const message = document.createElement("div");

  message.className = `message ${type}`;

  if (type === "user") {

    message.innerHTML = `
      <div class="bubble">
        ${escapeHtml(text)}
      </div>
    `;

  } else {

    message.innerHTML = `
      <div>
        <div class="message-label">KIO</div>
        <div class="bubble">
          ${escapeHtml(text)}
        </div>
      </div>
    `;

  }

  messages.appendChild(message);

  message.scrollIntoView({
    behavior: "smooth",
    block: "nearest"
  });
}

function startSession(text) {

  if (!text.trim()) return;

  startScreen.style.display = "none";
  chatSession.classList.add("active");

  addMessage("user", text);

  setTimeout(() => {

    addMessage(
      "ai",
      "Kio đã nhận task. Đây là nơi Kio sẽ phân tích yêu cầu, lập kế hoạch và thực hiện công việc."
    );

  }, 450);

  prompt.focus();
}

largeComposer.addEventListener("submit", (event) => {

  event.preventDefault();

  startSession(largePrompt.value);

  largePrompt.value = "";

});

composer.addEventListener("submit", (event) => {

  event.preventDefault();

  const text = prompt.value.trim();

  if (!text) return;

  addMessage("user", text);

  prompt.value = "";
  prompt.style.height = "42px";

  setTimeout(() => {

    addMessage(
      "ai",
      "Kio đã nhận task tiếp theo."
    );

  }, 350);

});

prompt.addEventListener("input", () => {

  prompt.style.height = "42px";

  prompt.style.height =
    Math.min(prompt.scrollHeight, 140) + "px";

});

largePrompt.addEventListener("input", () => {

  largePrompt.style.height = "75px";

  largePrompt.style.height =
    Math.min(largePrompt.scrollHeight, 110) + "px";

});

document.querySelectorAll("[data-prompt]").forEach(button => {

  button.addEventListener("click", () => {

    startSession(button.dataset.prompt);

  });

});

document.getElementById("newChat").addEventListener("click", () => {

  messages.innerHTML = "";

  chatSession.classList.remove("active");

  startScreen.style.display = "";

  largePrompt.value = "";

  prompt.value = "";

  closeSidebar();

});

document.querySelectorAll(".recent button").forEach(button => {

  button.addEventListener("click", () => {

    startSession(button.textContent.trim());

    closeSidebar();

  });

});
