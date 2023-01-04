function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteQuery(queryId) {
  fetch("/delete-query", {
    method: "POST",
    body: JSON.stringify({ queryId: queryId }),
  }).then((_res) => {
    window.location.href = "/queries";
  });
}