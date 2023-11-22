const serp = document.getElementsByClassName("cib-serp-main")[0];
const obj = serp.shadowRoot.getElementById("cib-action-bar-main");
const input = obj.shadowRoot.querySelector(".input-row").children[0];
const textarea = input.shadowRoot.children[0].getElementsByTagName("textarea")[0];

textarea.focus();
textarea.value = "{{content}}";
textarea.dispatchEvent(new Event("change"));

// send enter key
const event = new KeyboardEvent("keydown", {key: "Enter"});
textarea.dispatchEvent(event);
