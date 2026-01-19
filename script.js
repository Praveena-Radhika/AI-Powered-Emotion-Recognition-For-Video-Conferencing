document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded successfully!"); // Debugging step

    const signupBtn = document.getElementById("signupBtn");

    if (signupBtn) {
        console.log("Signup button found!"); // Debugging step

        signupBtn.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior
            console.log("Redirecting to dashboard.html..."); // Debugging step
            window.location.href = "dashboard.html"; // Redirect to the dashboard page
        });
    } else {
        console.log("Signup button not found!");
    }
});