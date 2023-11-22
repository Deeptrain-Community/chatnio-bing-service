window.getGroup = function getGroup() {
    const serp = document.getElementsByClassName("cib-serp-main")[0];
    const conversation = serp.shadowRoot.getElementById("cib-conversation-main");
    const chat = conversation.shadowRoot.querySelector("cib-chat-turn");
    const groups = chat.shadowRoot.querySelectorAll("cib-message-group");
    if (groups.length === 0) return null;

    return groups[groups.length - 1];
}

window.getText = function () {
    try {
        const group = getGroup();
        if (group === null) return null;

        const messages = [...group.shadowRoot.querySelectorAll('cib-message')];
        const data = messages.map((child) => {
            const shared = child.shadowRoot.children[0];

            return convertMarkdown(shared);
        })

        return data.join("\n");
    } catch (e) {
        console.debug(e);
        return null;
    }
}

window.convertMarkdown = function (el) {
    let resp = "";
    switch (el.tagName.toLowerCase()) {
        case "h1":
            return `# ${el.innerText}`;
        case "h2":
            return `## ${el.innerText}`;
        case "h3":
            return `### ${el.innerText}`;
        case "h4":
            return `#### ${el.innerText}`;
        case "h5":
            return `##### ${el.innerText}`;
        case "h6":
            return `###### ${el.innerText}`;
        case "img":
            return `![${el.alt}](${el.src})`;
        case "image":
            return `![${el.alt}](${el.src})`;
        case "a":
            return `[${el.innerText}](${el.href})`;
        case "ul":
            resp = "";
            for (const child of el.children) {
                resp += `- ${convertMarkdown(child)}`;
            }
            return resp;
        case "ol":
            resp = "";
            for (const child of el.children) {
                resp += `1. ${convertMarkdown(child)}`;
            }
            return resp;
        case "br":
            return `\n`;
        case "span":
            return el.innerText;
        case "strong":
            return `**${el.innerText}**`;
        case "em":
            return `*${el.innerText}*`;
        case "code":
            return `\`${el.innerText}\``;
        case "pre":
            return `\`\`\`\n${el.innerText}\n\`\`\``;
        case "blockquote":
            return `> ${el.innerText}`;
        case "hr":
            return `---`;
        case "table":
            resp = "";
            for (const child of el.children) {
                resp += `${convertMarkdown(child)}\n`;
            }
            return resp;
        case "thead":
            resp = "";
            for (const child of el.children) {
                resp += `${convertMarkdown(child)}\n`;
            }
            return resp;
        case "tbody":
            resp = "";
            for (const child of el.children) {
                resp += `${convertMarkdown(child)}\n`;
            }
            return resp;
        case "tr":
            resp = "";
            for (const child of el.children) {
                resp += `${convertMarkdown(child)}\n`;
            }
            return resp;
        case "th":
            return `| ${convertMarkdown(el)} `;
        case "td":
            return `| ${convertMarkdown(el)} `;
        default:
            if (el.children.length > 0)
                return [...el.children].map((child) => convertMarkdown(child)).join("");
            return el.innerText;
    }
}
