const noteInput = document.getElementById("noteInput");
const notesList = document.getElementById("notesList");

let editingId = null;

// Load saved notes
async function loadNotes() {
    try {
        const response = await fetch("/api/notes");
        const notes = await response.json();

        notesList.innerHTML = "";

        if (notes.length === 0) {
            notesList.textContent = "No notes saved yet.";
            return;
        }

        notes.forEach(note => {
            const card = document.createElement("div");
            card.className = "note-card";

            const date = document.createElement("div");
            date.className = "note-date";
            date.textContent = note.created_at;

            const content = document.createElement("p");
            content.textContent = note.content;

            const editBtn = document.createElement("button");
            editBtn.className = "edit-btn";
            editBtn.textContent = "✏️ Edit";
            editBtn.onclick = () => editNote(note.id, note.content);

            const deleteBtn = document.createElement("button");
            deleteBtn.className = "delete-btn";
            deleteBtn.textContent = "🗑️ Delete";
            deleteBtn.onclick = () => deleteNote(note.id);

            card.append(date, content, editBtn, deleteBtn);
            notesList.appendChild(card);
        });

    } catch (error) {
        notesList.textContent = "Unable to load notes.";
        console.error(error);
    }
}

// Save or update a note
async function saveNote() {
    const content = noteInput.value.trim();

    if (!content) {
        alert("Please write a note first!");
        return;
    }

    const url = editingId
        ? `/api/notes/${editingId}`
        : "/api/notes";

    const method = editingId ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: content })
        });

        if (!response.ok) {
            throw new Error("Unable to save note");
        }

        noteInput.value = "";
        editingId = null;
        document.getElementById("saveBtn").textContent = "💾 Save Note";

        await loadNotes();
        alert("Note saved successfully!");

    } catch (error) {
        alert(error.message);
    }
}

// Edit note
function editNote(id, content) {
    editingId = id;
    noteInput.value = content;

    document.getElementById("saveBtn").textContent = "Update Note";
    noteInput.focus();
}

// Delete note
async function deleteNote(id) {
    if (!confirm("Are you sure you want to delete this note?")) {
        return;
    }

    try {
        const response = await fetch(`/api/notes/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Unable to delete note");
        }

        await loadNotes();
        alert("Note deleted successfully!");

    } catch (error) {
        alert(error.message);
    }
}

// Load notes when page opens
loadNotes();