const log = console.log.bind(console)

const initRequest = callback => {
    const r = new XMLHttpRequest()
    r.responseType = 'json'
    r.onload = () => {
        if (r.status == 200) {
            callback(r.response)
        }
    }

    return r
}

const getJSONRequest = (path, callback) => {
    const r = initRequest(callback)
    r.open('GET', path)
    r.send()
}

const postJSONRequest = (path, data, callback) => {
    const r = initRequest(callback)
    r.open('POST', path)
    r.setRequestHeader('Content-Type', 'application/json')
    const body = JSON.stringify(data)
    r.send(body)
}

const e = (selector, element=document) => element.querySelector(selector)

const value = (selector, element=document) => {
    const input = e(selector, element)
    const v = input.value
    return v
}

const appendHTML = (selector, html) => {
    const element = e(selector)
    element.insertAdjacentHTML('beforeend', html)
}

const replaceHTML = (element, html) => {
    element.insertAdjacentHTML('afterend', html)
    element.remove()
}

const bind = (selector, eventType, callback) => {
    if (typeof selector == 'string') {
        const element = e(selector)
        element.addEventListener(eventType, callback)
    } else {
        const element = selector
        element.addEventListener(eventType, callback)
    }
}

Number.prototype.pad = function (width) {
    let s = String(this)
    s = s.padStart(width, '0')
    return s
}

const dateTime = (timestamp) => {
    timestamp *= 1000
    const d = new Date(timestamp)

    // const yyyy = d.getFullYear()
    // const mm = (d.getMonth() + 1).pad(2)
    // const dd = d.getDate().pad(2)

    const HH = d.getHours().pad(2)
    const MM = d.getMinutes().pad(2)
    const SS = d.getSeconds().pad(2)

    // const dt = `${yyyy}-${mm}-${dd} ${HH}:${MM}:${SS}`
    const dt = `${HH}:${MM}:${SS}`

    return dt
}

const delegate = (selector, eventType, className, callback) => {
    bind(selector, eventType, event => {
        const self = event.target
        if (self.classList.contains(className)) {
            callback(event)
        }
    })
}

const redirect = path => {
    setTimeout(() => {
        location.href = path
    }, 3000)
}