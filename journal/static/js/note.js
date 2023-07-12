function deleteNote(noteId) {
    fetch('notes/delete-note', {
        method : 'POST',
        body : JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = '/notes';
    })
}

function loginValidation(form) {
    fail = validateEmail(form.email.value)
    fail += validatePassword(form.password.value)

    if (fail == '') {
        return true
    }
    else { 
        alert(fail); return false

    }
}

function validateEmail(field) {
    if (field == '') {
        return 'No email was entered.\n'
    } else if (!((field.indexOf('.') > 0) &&
                (field.indexOf('@') > 0)) ||
                /[^a-zA-Z0-9.@_-]/.test(field))
        return 'The email address is invalid.\n'
    return ''
}

function validatePassword(field) {
    if (field == '') {
        return 'No password was entered.\n'
    } else if (field.length < 8) {
        return 'Password is too short'
    }
    return ''
}

