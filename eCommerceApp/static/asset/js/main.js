document.addEventListener("DOMContentLoaded", () => {
  // Check for stored theme preference and apply it
  const storedTheme = localStorage.getItem("theme");
  if (storedTheme) {
    document.body.classList.add(storedTheme);
    const themeIcon = document.getElementById("theme-icon");
    if (storedTheme === "dark-mode") {
      themeIcon.classList.remove("bi-sun-fill");
      themeIcon.classList.add("bi-moon-fill");
    }
  }

  // Add event listener to the theme toggle button
  document
    .getElementById("theme-toggle")
    .addEventListener("click", toggleTheme);
});

function toggleTheme() {
  // Toggle between light and dark mode
  const isDarkMode = document.body.classList.toggle("dark-mode");

  // Update the icon based on the theme
  const themeIcon = document.getElementById("theme-icon");
  if (isDarkMode) {
    themeIcon.classList.remove("bi-sun-fill");
    themeIcon.classList.add("bi-moon-fill");
    localStorage.setItem("theme", "dark-mode");
  } else {
    themeIcon.classList.remove("bi-moon-fill");
    themeIcon.classList.add("bi-sun-fill");
    localStorage.setItem("theme", "light-mode");
  }
}
