async function deleteTodo(todoId) {
    try {
        const response = await fetch(`/api/todos/${todoId}`, {
            method: 'DELETE',
            credentials: 'same-origin',
        });
        if (!response.ok) {
            alert(await response.text());
            if (response.status === 401) {
                window.location = '/login';
            }
            return;
        }
        document.querySelector(`li[data-todo-id='${todoId}']`).remove();
    } catch (e) {
        alert(e.message);
    }
}

async function updateTodo(todoId) {
    try {
        const response = await fetch(`/api/todos/${todoId}`, {
            method: 'UPDATE',
            credentials: 'same-origin',
        });
        if (!response.ok) {
            alert(await response.text());
            if (response.status === 401) {
                window.location = '/login';
            }
            return;
        }
    } catch (e) {
        alert(e.message);
    }
}