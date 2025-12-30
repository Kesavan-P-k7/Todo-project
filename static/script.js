document.addEventListener("DOMContentLoaded", loadTasks);

function toggleTheme() {
    document.body.classList.toggle("dark-theme");
}
function loadTasks() {
    fetch("/tasks")
        .then(res => res.json())
        .then(tasks => {
            const taskList = document.getElementById("taskList");
            taskList.innerHTML = "";

            tasks.forEach(task => {
                const li = document.createElement("li");

                li.innerHTML = `
                    <input type="checkbox" ${task.completed ? "checked" : ""} 
                        onchange="toggleTask(${task.id}, this.checked)">
                    <span class="${task.completed ? "completed" : ""}">
                        ${task.title}
                    </span>
                    <button onclick="deleteTask(${task.id})">❌</button>
                `;

                taskList.appendChild(li);
            });
        });
}

function addTask() {
    const input = document.getElementById("taskInput");
    const title = input.value.trim();

    if (!title) {
        alert("Task cannot be empty");
        return;
    }

    fetch("/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
    })
    .then(() => {
        input.value = "";
        loadTasks();
    });
}

function toggleTask(id, completed) {
    fetch(`/update/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed })
    }).then(loadTasks);
}

function deleteTask(id) {
    fetch(`/delete/${id}`, { method: "DELETE" })
        .then(loadTasks);
}
// ✅ Update task checkbox status