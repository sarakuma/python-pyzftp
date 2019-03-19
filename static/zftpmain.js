var selectTextElem = document.getElementsByName("machine-input")

//updateTextPlaceholderValue function to flip the placeholder text according to the user selection
function updateTextPlaceholderValue() {

    let selectElem = document.getElementById("machine-sel")
    let selectValue = selectElem.value
    console.log(selectValue)

    if (selectValue == "hostname") {
        selectTextElem[0].placeholder = "enter your hostname"
    } else {
        selectTextElem[0].placeholder = "enter your ip address"
    }

    return
}

document.getElementsByName("btnm")[0].onmouseover = function () { changeBtnmcursor() }

//changeBtnmcursor function to disable/enable the - button when the max limit is reached
function changeBtnmcursor() {

    let childcnt = document.getElementById("zftp-form").children.length

    //console.log(childcnt)

    if (childcnt > 4) {
        document.getElementsByName("btnm")[0].disabled = false
        document.getElementsByName("btnm")[0].style.cursor = "pointer"
    } else {
        document.getElementsByName("btnm")[0].disabled = true
        document.getElementsByName("btnm")[0].style.cursor = "default"
    }

}

//function to disable/enable the + button when the max limit is reached
document.getElementsByName("btnp")[0].onmouseover = function () {

    let childcnt = document.getElementById("zftp-form").children.length

    if (childcnt < 13) {
        document.getElementsByName("btnp")[0].disabled = false
        document.getElementsByName("btnp")[0].style.cursor = "pointer"
    } else {
        document.getElementsByName("btnp")[0].disabled = true
        document.getElementsByName("btnp")[0].style.cursor = "default"
    }


}

//function to add the DOM elements when + button is clicked
document.getElementsByName("btnp")[0].onclick = function () {

    //console.log("add..")

    let childcnt = document.getElementById("zftp-form").children.length
    let curchild = childcnt - 2

    if (childcnt < 13) {
        let article = document.createElement("article")

        article.className = "article-container"

        article.innerHTML = `
        <input type="hidden" name="trsfrno${curchild}" value=${curchild}>
        <span>FT#</span>
        <span>${curchild}</span>
        <fieldset>
            <legend>Verb?</legend>
            <div>
                <input type="radio" name="ftpverb-radio${curchild}" value="receive" checked>
                <label for="ftpverb-radio${curchild}">Recieve data from mainframe</label>
            </div>
            <div>
                <input type="radio" name="ftpverb-radio${curchild}" value="send">
                <label for="ftpverb-radio${curchild}">Send data to mainframe</label>
            </div>
        </fieldset>
        <fieldset>
             <legend>Format?</legend>
             <div>
                 <input type="radio" name="ftpformat-radio${curchild}" value="text" checked>
                 <label for="ftpformat-radio${curchild}">Text</label>
             </div>
             <div>
                 <input type="radio" name="ftpformat-radio${curchild}" value="binary">
                 <label for="ftpformat-radio${curchild}">Binary</label>
             </div>
        </fieldset>
        <fieldset>
            <legend>Files?</legend>
            <div>
                <input type=text name="dsn${curchild}" maxlength=44 placeholder="Mainframe dataset name" title="Please enter DSN without quotes" required>
            </div>
            <div>
                <input type=text name="filename${curchild}" placeholder="Client file name" title="Please specify the absolute path of the file" required>
            </div>
        </fieldset>
        `

        document.getElementById("zftp-form").appendChild(article)
        document.getElementsByName("btnm")[0].disabled = false
        document.getElementsByName("btnm")[0].style.cursor = "pointer"
    } else {
        document.getElementsByName("btnp")[0].disabled = true
        document.getElementsByName("btnp")[0].style.cursor = "default"
    }

}

//function to remove the DOM elements when - button is clicked
document.getElementsByName("btnm")[0].onclick = function () {

    //console.log("remove..")

    let form = document.getElementById("zftp-form")
    form.removeChild(form.lastChild)

    changeBtnmcursor()

    if (document.getElementsByName("btnp")[0].disabled) {
        document.getElementsByName("btnp")[0].disabled = false
        document.getElementsByName("btnp")[0].style.cursor = "pointer"
    }

}

window.onload = function () {

    let form = document.getElementById("zftp-form")
    let article3 = form.getElementsByTagName("article")[2]
    article3.style.paddingBottom = "0px"
}
