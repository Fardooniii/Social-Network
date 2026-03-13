document.addEventListener("DOMContentLoaded", function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const postForm = document.querySelector("#post-form");
    if (postForm) {
        postForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const content = document.querySelector("#post-content").value;
            fetch("/create/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: `content=${encodeURIComponent(content)}`
            }).then(() => location.reload());
        });
    }

    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function() {
            const postDiv = this.closest(".post");
            const postId = postDiv.dataset.postId;
            const contentP = postDiv.querySelector("p");
            const currentContent = contentP.innerText;

            contentP.innerHTML = `<textarea class="edit-content" style="width:100%;">${currentContent}</textarea>
                                  <button class="save-btn btn btn-primary btn-sm">Save</button>`;

            contentP.querySelector(".save-btn").addEventListener("click", function() {
                const newContent = contentP.querySelector(".edit-content").value;
                fetch(`/edit/${postId}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: `content=${encodeURIComponent(newContent)}`
                })
                .then(response => response.json())
                .then(result => {
                    if(result.success){
                        contentP.innerText = result.content;
                    } else {
                        alert(result.error || "Error updating post");
                    }
                });
            });
        });
    });

    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            const postDiv = this.closest(".post");
            const postId = postDiv.dataset.postId;
            const likesCount = this.querySelector(".likes-count");

            fetch(`/like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                likesCount.innerText = data.count;
                this.classList.toggle("liked", data.liked);
            });
        });
    });

    document.querySelectorAll(".comment-btn").forEach(button => {
        button.addEventListener("click", function() {
            const postDiv = this.closest(".post");
            const postId = postDiv.dataset.postId;
            let existingForm = postDiv.querySelector(".comment-form");
            if (existingForm) {
                existingForm.classList.toggle("d-none");
                return;
            }

            const form = document.createElement("form");
            form.classList.add("comment-form", "mt-2");
            form.innerHTML = `
                <input type="text" class="form-control mb-1 comment-content" placeholder="Write a comment..." required>
                <button type="submit" class="btn btn-sm btn-primary">Post</button>
            `;
            postDiv.appendChild(form);

            form.addEventListener("submit", function(e) {
                e.preventDefault();
                const content = form.querySelector(".comment-content").value;
                fetch(`/comment/${postId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: `content=${encodeURIComponent(content)}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const commentDiv = document.createElement("div");
                        commentDiv.classList.add("mt-1");
                        commentDiv.innerHTML = `<strong>${data.username}</strong>: ${data.content} <span class="text-muted">(${data.timestamp})</span>`;
                        form.before(commentDiv);
                        form.querySelector(".comment-content").value = "";
                    } else {
                        alert(data.error || "Failed to post comment");
                    }
                });
            });
        });
    });
});