// File: static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const commentsList = document.getElementById('comments-list');

    commentsList.addEventListener('click', async (event) => {
        const likeButton = event.target.closest('.like-button');
        if (likeButton) {
            const commentId = likeButton.dataset.commentId;
            const userId = 'user123'; // This would come from a user session in a real app

            let url = '';
            let method = 'POST';

            // Check if the user has already liked the comment (visual state)
            const isLiked = likeButton.classList.contains('liked');

            if (isLiked) {
                url = `/api/unlike/${commentId}`;
            } else {
                url = `/api/like/${commentId}`;
            }

            try {
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_id: userId })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if (data.comment) {
                    // Update the like count and button style
                    const likeCountSpan = likeButton.querySelector('.like-count');
                    likeCountSpan.textContent = data.comment.likes;

                    if (isLiked) {
                        likeButton.classList.remove('liked');
                    } else {
                        likeButton.classList.add('liked');
                    }
                }
            } catch (error) {
                console.error('Error liking/unliking comment:', error);
            }
        }
    });
});

async function sortComments(sortBy) {
    let url = '/api/comments';
    if (sortBy === 'popularity') {
        url += '?sort_by=popularity';
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const comments = await response.json();
        updateCommentsDisplay(comments);
    } catch (error) {
        console.error('Error fetching and sorting comments:', error);
    }
}

function updateCommentsDisplay(comments) {
    const commentsListDiv = document.getElementById('comments-list');
    commentsListDiv.innerHTML = ''; // Clear current comments

    for (const commentId in comments) {
        const comment = comments[commentId];
        const commentCard = document.createElement('div');
        commentCard.className = 'comment-card';
        commentCard.id = `comment-${commentId}`;
        commentCard.innerHTML = `
            <p>${comment.text}</p>
            <div class="comment-actions">
                <button class="like-button" data-comment-id="${commentId}">
                    <span class="heart-icon">&#x2665;</span> <span class="like-count">${comment.likes}</span> Like
                </button>
            </div>
        `;
        commentsListDiv.appendChild(commentCard);
    }
}
