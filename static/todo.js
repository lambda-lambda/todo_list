const todoApi = {}

todoApi.add = (content, callback) => {
    const todo = {
        content: content
    }
    const path = '/api/todo/add'
    postJSONRequest(path, todo, callback)
}

todoApi.all = callback => {
    const path = '/api/todo/all'
    getJSONRequest(path, callback)
}

todoApi.delete = (id, callback) => {
    const path = `/api/todo/delete?id=${id}`
    getJSONRequest(path, callback)
}

todoApi.update = (id, content, callback) => {
    const path = '/api/todo/update'
    const todo = {
        id: id,
        content: content,
    }

    postJSONRequest(path, todo, callback)
}

const todoView = {}

const templateTodo = (todo) => {
    const t = `
        <div class="todo-item" data-id="${todo.id}" data-content="${todo.content}">
            <button class="todo-delete">删除</button>
            <button class="todo-edit">编辑</button>
            <div class="todo-created-time">${dateTime(todo.created_time)}</div>
            <div class="todo-content">${todo.content}</div>
        </div>
    `
    return t
}

todoView.add = (todo) => {
    const html = templateTodo(todo)
    appendHTML('#id-div-todo-list', html)
}

todoView.all = (todos) => {
    for (const todo of todos) {
        todoView.add(todo)
    }
}

todoView.delete = (todoItem) => {
    todoItem.remove()
}

const todoEvent = {}

todoEvent.add = () => {
    bind('#id-input-todo-content', 'keypress', event => {
        if (event.key == 'Enter') {
            const self = event.target
            const content = self.value
            todoApi.add(content, todo => todoView.add(todo))
        }
    })
}

todoEvent.all = () => {
    bind(document, 'DOMContentLoaded', event => {
        todoApi.all(todos => todoView.all(todos))
    })
}

todoEvent.delete = () => {
    delegate('#id-div-todo-list', 'click', 'todo-delete', event => {
        const self = event.target
        const todoItem = self.closest('.todo-item')
        const id = todoItem.dataset.id
        todoApi.delete(id, todo => {
            todoView.delete(todoItem)
        })
    })
}

const templateTodoUpdateForm = content => {
    const t = `
        <div class="todo-update-form">
            <input type="text" class="todo-content" value="${content}">
            <button class="todo-cancle-update">取消</button>
            <button class="todo-update">更新</button>
        </div>
    `
    return t
}

todoEvent.edit = () => {
    delegate('#id-div-todo-list', 'click', 'todo-edit', event => {
        const self = event.target
        const todoItem = self.closest('.todo-item')
        const content = todoItem.dataset.content
        const todoContentDiv = e('div.todo-content', todoItem)
        if (todoContentDiv != null) {
            const html = templateTodoUpdateForm(content)
            replaceHTML(todoContentDiv, html)
        } else {
            log('不要重复点击编辑按钮')
        }
    })
}

const templateTodoContent = content => {
    const t = `<div class="todo-content">${content}</div>`
    return t
}

todoEvent.cancleUpdate = () => {
    delegate('#id-div-todo-list', 'click', 'todo-cancle-update', event => {
        const self = event.target
        const todoItem = self.closest('.todo-item')
        const content = todoItem.dataset.content
        const todoUpdateForm = e('.todo-update-form', todoItem)
        const html = templateTodoContent(content)
        replaceHTML(todoUpdateForm, html)
    })
}

todoEvent.update = () => {
    delegate('#id-div-todo-list', 'click', 'todo-update', event => {
        const self = event.target
        const todoItem = self.closest('.todo-item')
        const contentInput = e('.todo-content', todoItem)
        const content = contentInput.value
        const id = Number(todoItem.dataset.id)

        todoApi.update(id, content, todo => {
            const html = templateTodo(todo)
            replaceHTML(todoItem, html)
        })
    })
}

todoEvent.init = () => {
    todoEvent.add()
    todoEvent.all()
    todoEvent.delete()
    todoEvent.edit()
    todoEvent.cancleUpdate()
    todoEvent.update()
}

const __main__ = () => {
    todoEvent.init()
}

__main__()