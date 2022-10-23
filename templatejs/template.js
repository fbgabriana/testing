window.addEventListener("DOMContentLoaded", (event) => {
	fetch("template.html").then(response => {
		return response.text();
	}).then(str => {
		let parser = new DOMParser();
		let template = parser.parseFromString(str, "text/html");

		template.querySelector("#content").replaceWith(document.querySelector("#content"));
		template.title = template.title.replace("${title}", document.title);
		document.documentElement.replaceWith(template.documentElement);
	}).catch(error => {  
		console.log(error);  
	});
});
