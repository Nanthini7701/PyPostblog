// static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("form.inline-like").forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const url = form.action;
      const csrftoken = form.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;
      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((r) => r.json())
        .then((data) => {
          form.querySelector(".like-count").textContent = data.total_likes;
          form.querySelector(".like-btn").classList.toggle("liked", data.liked);
        })
        .catch((err) => console.error(err));
    });
  });
});
