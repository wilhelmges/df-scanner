document.addEventListener("DOMContentLoaded", () => {

    const sidebar = document.querySelector(".sidebar-nav");

    if (!sidebar) {
        return;
    }

    const item = document.createElement("li");

    item.innerHTML = `
        <a href="/getupdates">
            <span class="nav-link-title">
                Оновлення
            </span>
        </a>
    `;

    sidebar.appendChild(item);
});