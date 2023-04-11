const data = document.currentScript.dataset;
const url = data.url;
const commentText = document.getElementById("id_text");
const tagsDiv = document.getElementById("tags");


function buildHtml(array) {
    let div = document.createElement("div")
    div.classList.add("row", "text-primary")
    for (let i = 0; i < array.length; i++) {
        let tag = document.createElement("a")
        tag.classList.add("col", "text-decoration-none")
        tag.role = "button"
        tag.innerHTML = '#' + array[i]
        div.append(tag)
    }
    return div
}

function searchWord(word, array) {
    /* Returns an array of matching hashtags */
    let output = [];
    if (word.length > 2) {
        for (let i = 0; i < array.length; i++) {
            if (array[i].substr(0, word.length).toUpperCase() == word.toUpperCase()) {
                output.push(array[i])
            }
        }
    }
    return output
}

function readInput(input, array, parent, result_count) {
    input.addEventListener("input", function (e) {
        const textArray = this.value.split(' ');
        let matches = [];
        for (let i = 0; i < textArray.length; i++) {
            matches = matches.concat((searchWord(textArray[i], array)))
        }
        distinctMatches = [...new Set(matches)].slice(0, result_count);
        if (!distinctMatches.length == 0) {
            parent.innerHTML = buildHtml(distinctMatches).outerHTML
        } else {
            parent.innerHTML = "Topic suggestions appear here"
        }
    })
}


function getTags() {
    fetch(url, {
        method: 'get',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status == 'success') {
                const issues = data.issues;
                readInput(commentText, issues, tagsDiv, 5);
            }
            console.log(data);
        })
        .catch((error) => {
            console.error(error);
        })
}

tagsDiv.addEventListener("click", function (e) {
    let a = e.target.closest('a');
    if (!a) return;
    if (!tagsDiv.contains(a)) return;
    commentText.value += (" " + a.innerText + " ");
    commentText.focus()
})

getTags()
