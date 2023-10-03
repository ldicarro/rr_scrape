window.addEventListener('DOMContentLoaded', init);

var gptResumeText;
var gptLetterText;
var gptIntentText;

function init() {
    document.querySelectorAll('.post').forEach(el => {
        // open post
        el.addEventListener('click', handlePostClick);
        
        // if post is not null, highlight other posts with same id
        // when headline is clicked
        let headlineElement = el.querySelector('.post__headline');
        if(headlineElement) {
            headlineElement.addEventListener('click', handleHeadlineClick)
        }
    });
    document.querySelectorAll('.getSSText').forEach(el => el.addEventListener('click',getSSText));
    document.querySelectorAll('.getGPTText').forEach(el => el.addEventListener('click',getGPTText));
    document.querySelectorAll('.getGPTRes').forEach(el => el.addEventListener('click',getGPTResText));
    document.querySelectorAll('.getGPTLtr').forEach(el => el.addEventListener('click',getGPTLtrText));
    document.querySelectorAll('.getGPTInt').forEach(el => el.addEventListener('click',getGPTIntText));
    document.querySelectorAll('.close').forEach(el => el.addEventListener('click',hidePost));
    document.querySelectorAll('.tabs > h2').forEach(el => el.addEventListener('click',switchTab));

    document.querySelectorAll('.tabs > h2')[0].classList.add('active');
    document.querySelectorAll('.posts__content')[0].classList.add('show');
}

function handlePostClick(evt) {
    let el;

    if (!evt.target.classList.contains("post")) {
        el = evt.target.closest("div.post")
    }
    else {
        el = evt.target;
    }

    if(el.dataset.visible === 'true') {
        return;
    }
    
    el.classList.add('viewed')
    el.querySelector('.post__description').classList.add('show');
    el.querySelector('a').classList.add('show');
    el.querySelector('.close').classList.add('close-show');
    el.dataset.visible = 'true';
}

function handleHeadlineClick(evt) {
    let el;

    if (!evt.target.classList.contains("post")) {
        el = evt.target.closest("div.post")
    }
    else {
        el = evt.target;
    }

    if(el.dataset.visible === 'false') {
        return;
    }
    
    // find matching posts and add class
    // to know it has been clicked
    document.querySelectorAll('.post').forEach(post => {
        if(post.dataset.id == el.dataset.id) {
            post.classList.add('applied')
        }
    })
}

function hidePost(evt) {
    let el = evt.target.closest("div.post");
    
    el.querySelector('.post__description').classList.remove('show');
    el.querySelector('a').classList.remove('show');
    el.querySelector('.close').classList.remove('close-show');
    el.dataset.visible = 'false';
    evt.stopPropagation();
}

function getSSText(evt) {
    const el = evt.target.closest("div.post");
    const table = el.querySelector('table');

    let clipboardText = '';
    Array.from(table.rows.item(0).cells).forEach(c => clipboardText += c.textContent + '\t');
    navigator.clipboard.writeText(clipboardText);
}

function getGPTText(evt) {
    const el = evt.target.closest("div.post");
    const company = el.querySelector('.post__headline > h4').textContent;
    const position = el.querySelector('.post__headline > .post__headline--link > a > h3').textContent;
    const jd = el.querySelector('.post__description').textContent;

    const data = {
        "company": company,
        "position": position,
        "jobDescription": jd
    }

    fetch("https://192.168.0.130:1993/gpt", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(res => res.json())
        .then(json => {
            gptResumeText = json.resume;
            gptLetterText = json.coverletter;
            gptIntentText = json.companyinterest;
            el.querySelector('.post__buttonbar--secondary').classList.add('show');
        });
}

function getGPTResText(evt) {
    if(gptResumeText === '') {
        return;
    }

    navigator.clipboard.writeText(gptResumeText);
}

function getGPTLtrText(evt) {
    if(gptLetterText === '') {
        return;
    }

    navigator.clipboard.writeText(gptLetterText);
}

function getGPTIntText(evt) {
    if(gptIntentText === '') {
        return;
    }

    navigator.clipboard.writeText(gptIntentText);
}

function switchTab(evt) {
    const tabs = Array.from(document.querySelectorAll('.tabs > h2'));
    const newTabIndex = tabs.indexOf(evt.currentTarget);

    const panes = document.querySelectorAll('.posts__content');

    tabs.forEach(tab => tab.classList.remove('active'));
    tabs[newTabIndex].classList.add('active');

    panes.forEach(el => el.classList.remove('show'));
    panes[newTabIndex].classList.add('show');
    
}