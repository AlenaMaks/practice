const avatarBtn =
    document.getElementById("avatar-btn");

const sidebarMenu =
    document.getElementById("sidebar-menu");


if (avatarBtn && sidebarMenu) {

    avatarBtn.addEventListener(
        "click",
        function(event) {

            event.stopPropagation();

            sidebarMenu.classList.toggle(
                "active"
            );
        }
    );

    document.addEventListener(
        "click",
        function(event) {

            if (
                !sidebarMenu.contains(event.target)
            ) {
                sidebarMenu.classList.remove(
                    "active"
                );
            }
        }
    );

}