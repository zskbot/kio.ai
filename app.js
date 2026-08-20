const startScreen =
document.getElementById("startScreen");

const chatScreen =
document.getElementById("chatScreen");

const skillsPage =
document.getElementById("skillsPage");

const pluginsPage =
document.getElementById("pluginsPage");

const toolsPage =
document.getElementById("toolsPage");

const startForm =
document.getElementById("startForm");

const startInput =
document.getElementById("startInput");

const chatForm =
document.getElementById("chatForm");

const chatInput =
document.getElementById("chatInput");

const messages =
document.getElementById("messages");

const consoleBox =
document.getElementById("console");

const planBox =
document.getElementById("plan");

const filesBox =
document.getElementById("files");

const activeSkills =
document.getElementById("activeSkills");

const agentStatus =
document.getElementById("agentStatus");

const pageTitle =
document.getElementById("pageTitle");

const taskList =
document.getElementById("taskList");

const menuBtn =
document.getElementById("menuBtn");

const agentPanel =
document.querySelector(".agent-panel");

let activeTask = false;
let socket = null;


function escapeHtml(value) {

return String(value)
.replaceAll("&","&amp;")
.replaceAll("<","&lt;")
.replaceAll(">","&gt;")
.replaceAll('"',"&quot;")
.replaceAll("'","&#039;");

}


function scrollMessages() {

messages.scrollTop =
messages.scrollHeight;

}


function scrollConsole() {

consoleBox.scrollTop =
consoleBox.scrollHeight;

}


function addUserMessage(text) {

const el =
document.createElement("div");

el.className =
"message user";

el.innerHTML = `
<div class="user-bubble">
${escapeHtml(text)}
</div>
`;

messages.appendChild(el);

scrollMessages();

}


function addAgentMessage(text) {

const el =
document.createElement("div");

el.className =
"message";

el.innerHTML = `
<div class="agent-message">
<div class="agent-label">KIO</div>
<div class="agent-bubble">
${escapeHtml(text)}
</div>
</div>
`;

messages.appendChild(el);

scrollMessages();

}


function addLog(event) {

const el =
document.createElement("div");

el.className =
"log " +
(
event.level === "error"
? "error"
: event.message.startsWith("✓")
? "success"
: ""
);

el.textContent =
`[${event.time}] ${event.message}`;

consoleBox.appendChild(el);

scrollConsole();

}


function setPlan(items) {

planBox.innerHTML = "";

items.forEach((item,index) => {

const el =
document.createElement("div");

el.className =
"plan-item" +
(index === 0 ? " active" : "");

el.innerHTML = `
<span class="plan-dot"></span>
<span>${escapeHtml(item)}</span>
`;

planBox.appendChild(el);

});

}


function setFiles(files) {

filesBox.innerHTML = "";

files.slice(0,60).forEach(file => {

const el =
document.createElement("div");

el.className =
"file-item";

el.innerHTML = `
<span>◇</span>
<span>${escapeHtml(file.path)}</span>
<span class="file-status ${file.status}">
${file.status}
</span>
`;

filesBox.appendChild(el);

});

}


function setActiveSkills(skills) {

activeSkills.innerHTML = "";

skills.forEach(skill => {

const el =
document.createElement("div");

el.className =
"skill-chip";

el.innerHTML = `
<span>◇</span>
${escapeHtml(skill)}
`;

activeSkills.appendChild(el);

});

}


function addTask(text) {

if (
taskList.children.length === 1 &&
taskList.children[0].classList.contains("empty")
) {

taskList.innerHTML = "";

}

const item =
document.createElement("div");

item.className =
"task-item";

item.textContent = text;

taskList.prepend(item);

}


function showChat() {

startScreen.style.display = "none";

skillsPage.classList.remove("active");

pluginsPage.classList.remove("active");

if (toolsPage) {
toolsPage.classList.remove("active");
}

chatScreen.classList.add("active");

pageTitle.textContent =
"Active session";

document
.querySelectorAll(".nav-item")
.forEach(x => x.classList.remove("active"));

document
.querySelector('[data-page="chat"]')
.classList.add("active");

}


async function sendTask(text) {

text = text.trim();

if (!text || activeTask) return;

activeTask = true;

showChat();

addUserMessage(text);

addTask(text);

agentStatus.textContent =
"WORKING";

consoleBox.innerHTML = "";

try {

const response =
await fetch("/api/task",{

method:"POST",

headers:{
"Content-Type":
"application/json"
},

body:JSON.stringify({
task:text
})

});

const data =
await response.json();

if (!response.ok) {

throw new Error(
data.error ||
"Task failed"
);

}

} catch(error) {

addLog({
time:new Date().toLocaleTimeString(),
message:"✗ " + error.message,
level:"error"
});

addAgentMessage(
"Không thể kết nối KIO Agent backend."
);

agentStatus.textContent =
"ERROR";

activeTask = false;

}

}


function resetWorkspace() {

activeTask = false;

chatScreen.classList.remove("active");

skillsPage.classList.remove("active");

pluginsPage.classList.remove("active");

startScreen.style.display = "";

messages.innerHTML = "";

consoleBox.innerHTML = "";

planBox.innerHTML =
`<div class="empty">Waiting for task</div>`;

filesBox.innerHTML =
`<div class="empty">No files selected</div>`;

activeSkills.innerHTML =
`<div class="empty">No skills selected</div>`;

taskList.innerHTML =
`<div class="empty">No active tasks</div>`;

agentStatus.textContent =
"IDLE";

pageTitle.textContent =
"New session";

startInput.value = "";

chatInput.value = "";

}


function showPage(page) {

startScreen.style.display = "none";

chatScreen.classList.remove("active");

skillsPage.classList.remove("active");

pluginsPage.classList.remove("active");

if (toolsPage) {
toolsPage.classList.remove("active");
}

document
.querySelectorAll(".nav-item")
.forEach(x =>
x.classList.remove("active")
);

if(page === "chat") {

chatScreen.classList.add("active");

pageTitle.textContent =
"Chat";

document
.querySelector('[data-page="chat"]')
.classList.add("active");

}

if(page === "skills") {

skillsPage.classList.add("active");

pageTitle.textContent =
"Skills";

document
.querySelector('[data-page="skills"]')
.classList.add("active");

}

if(page === "tools") {

if (toolsPage) {
toolsPage.classList.add("active");
}

pageTitle.textContent =
"Tools";

document
.querySelector('[data-page="tools"]')
.classList.add("active");

}

if(page === "plugins") {

pluginsPage.classList.add("active");

pageTitle.textContent =
"Plugins";

document
.querySelector('[data-page="plugins"]')
.classList.add("active");

}

closeMobileMenu();

}


function closeMobileMenu() {

if(agentPanel) {

agentPanel.classList.remove(
"mobile-open"
);

}

}


function renderSkills(skills) {

const grid =
document.getElementById("skillsGrid");

grid.innerHTML = "";

skills.forEach(skill => {

const card =
document.createElement("div");

card.className =
"card";

card.innerHTML = `
<div class="card-icon">
${escapeHtml(skill.icon)}
</div>

<h3>
${escapeHtml(skill.name)}
</h3>

<p>
${escapeHtml(skill.description)}
</p>

<div class="card-meta">

<span class="status connected">
AVAILABLE
</span>

<button
class="card-btn"
data-skill="${escapeHtml(skill.id)}"
>
Use skill
</button>

</div>
`;

grid.appendChild(card);

});

}


function renderTools(tools) {

const grid =
document.getElementById("toolsGrid");

if (!grid) return;

grid.innerHTML = "";

tools.forEach(tool => {

const card =
document.createElement("div");

card.className =
"card";

card.innerHTML = `
<div class="card-icon">
${escapeHtml(tool.icon)}
</div>

<h3>
${escapeHtml(tool.name)}
</h3>

<p>
${escapeHtml(tool.description)}
</p>

<div class="card-meta">

<span class="status connected">
AVAILABLE
</span>

<button
class="card-btn tool-use"
data-tool="${escapeHtml(tool.id)}"
>
Use tool
</button>

</div>
`;

grid.appendChild(card);

});

}

function showToolActivity(tool) {

showChat();

addLog({
time:new Date().toLocaleTimeString(),
message:"→ tool:" + tool,
level:"info"
});

addAgentMessage(
"Tool selected: " + tool
);

}

function renderPlugins(plugins) {

const grid =
document.getElementById("pluginsGrid");

grid.innerHTML = "";

plugins.forEach(plugin => {

const card =
document.createElement("div");

card.className =
"card";

card.innerHTML = `
<div class="card-icon">
◆
</div>

<h3>
${escapeHtml(plugin.name)}
</h3>

<p>
${escapeHtml(plugin.description)}
</p>

<div class="card-meta">

<span
class="status"
data-plugin-status="${escapeHtml(plugin.id)}"
>
${escapeHtml(plugin.status)}
</span>

<button
class="card-btn plugin-btn"
data-plugin="${escapeHtml(plugin.id)}"
>
Connect
</button>

</div>
`;

grid.appendChild(card);

});

}


async function loadManagementData() {

try {

const skills =
await fetch("/api/skills")
.then(r => r.json());

renderSkills(skills);

} catch {}

try {

const plugins =
await fetch("/api/plugins")
.then(r => r.json());

renderPlugins(plugins);

} catch {}

}


function connectSocket() {

const protocol =
location.protocol === "https:"
? "wss:"
: "ws:";

socket =
new WebSocket(
`${protocol}//${location.host}/ws`
);

socket.onmessage =
event => {

const data =
JSON.parse(event.data);

if(data.type === "log") {

addLog(data);

}

else if(data.type === "activity") {

agentStatus.textContent =
data.status === "done"
? "DONE"
: "WORKING";

}

else if(data.type === "plan") {

setPlan(data.items);

}

else if(data.type === "skills") {

setActiveSkills(
data.skills
);

}

else if(data.type === "files") {

setFiles(data.files);

}

else if(data.type === "agent") {

addAgentMessage(
data.message
);

}

else if(data.type === "complete") {

agentStatus.textContent =
"DONE";

activeTask = false;

scrollMessages();

scrollConsole();

}

};

socket.onclose =
() => {

setTimeout(
connectSocket,
1000
);

};

}


startForm.addEventListener(
"submit",
event => {

event.preventDefault();

const text =
startInput.value;

startInput.value = "";

startInput.style.height =
"82px";

sendTask(text);

});


chatForm.addEventListener(
"submit",
event => {

event.preventDefault();

const text =
chatInput.value;

chatInput.value = "";

chatInput.style.height =
"42px";

sendTask(text);

});


startInput.addEventListener(
"input",
() => {

startInput.style.height =
"82px";

startInput.style.height =
Math.min(
startInput.scrollHeight,
110
) + "px";

});


chatInput.addEventListener(
"input",
() => {

chatInput.style.height =
"42px";

chatInput.style.height =
Math.min(
chatInput.scrollHeight,
140
) + "px";

});


document
.querySelectorAll("[data-task]")
.forEach(button => {

button.addEventListener(
"click",
() => {

sendTask(
button.dataset.task
);

});

});


document
.querySelectorAll(".nav-item")
.forEach(button => {

button.addEventListener(
"click",
() => {

showPage(
button.dataset.page
);

});

});


document
.getElementById("newSession")
.addEventListener(
"click",
resetWorkspace
);


document
.addEventListener(
"click",
event => {

const toolButton =
event.target.closest(
".tool-use"
);

if(toolButton) {

showToolActivity(
toolButton.dataset.tool
);

}


const pluginButton =
event.target.closest(
".plugin-btn"
);

if(pluginButton) {

const status =
document.querySelector(
`[data-plugin-status="${pluginButton.dataset.plugin}"]`
);

if(
status.classList.contains("connected")
) {

status.textContent =
"DISCONNECTED";

status.classList.remove(
"connected"
);

pluginButton.textContent =
"Connect";

} else {

status.textContent =
"CONNECTED";

status.classList.add(
"connected"
);

pluginButton.textContent =
"Connected";

}

}


const skillButton =
event.target.closest(
"[data-skill]"
);

if(skillButton) {

const skill =
skillButton.dataset.skill;

showChat();

addAgentMessage(
`Skill selected: ${skill}`
);

}

});


if(menuBtn) {

menuBtn.addEventListener(
"click",
event => {

event.stopPropagation();

agentPanel.classList.toggle(
"mobile-open"
);

});

}


document.addEventListener(
"click",
event => {

if(
window.innerWidth <= 750 &&
agentPanel &&
agentPanel.classList.contains(
"mobile-open"
) &&
!agentPanel.contains(event.target) &&
event.target !== menuBtn
) {

closeMobileMenu();

}

});


loadManagementData();

connectSocket();

/* ==========================================
   KIO PLUGIN MANAGER
========================================== */

async function refreshPlugins() {

try {

const plugins =
await fetch("/api/plugins")
.then(r => r.json());

renderPlugins(plugins);

} catch(error) {

console.error(
"KIO plugin registry:",
error
);

}

}


function renderPlugins(plugins) {

const grid =
document.getElementById(
"pluginsGrid"
);

if (!grid) return;

grid.innerHTML = "";

plugins.forEach(plugin => {

const card =
document.createElement("div");

card.className = "card";

const configured =
plugin.configured === true;

card.innerHTML = `

<div class="card-icon">
◆
</div>

<h3>
${escapeHtml(plugin.name)}
</h3>

<p>
${escapeHtml(plugin.description)}
</p>

<div class="card-meta">

<span
class="status ${configured ? "connected" : ""}"
>
${configured
? "CONNECTED"
: "NOT CONFIGURED"}
</span>

<button
class="card-btn plugin-call"
data-plugin="${escapeHtml(plugin.id)}"
>
${configured
? "Test"
: "Configure"}
</button>

</div>

`;

grid.appendChild(card);

});

}


async function callKioPlugin(plugin) {

try {

const response =
await fetch(
"/api/plugin/call",
{
method:"POST",
headers:{
"Content-Type":
"application/json"
},
body:JSON.stringify({
plugin:plugin,
action:"status"
})
}
);

const result =
await response.json();

showPage("chat");

addLog({
time:
new Date().toLocaleTimeString(),
message:
result.ok
? `✓ plugin:${plugin} READY`
: `! plugin:${plugin} ${result.status || "ERROR"}`,
level:
result.ok
? "success"
: "error"
});

addAgentMessage(
result.ok
? `Plugin ${plugin} is ready for KIO Agent.`
: `Plugin ${plugin} chưa được cấu hình credential.`
);

} catch(error) {

addLog({
time:
new Date().toLocaleTimeString(),
message:
"✗ plugin call failed",
level:"error"
});

}

}


document.addEventListener(
"click",
event => {

const button =
event.target.closest(
".plugin-call"
);

if(!button) return;

callKioPlugin(
button.dataset.plugin
);

}
);

refreshPlugins();
