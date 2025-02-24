// Example JavaScript (can be expanded for dynamic features)
document.addEventListener('DOMContentLoaded', function() {
    console.log("Blog application loaded successfully!");

    // Example: Highlight posts on hover
    const posts = document.querySelectorAll('.post');
    posts.forEach(post => {
        post.addEventListener('mouseover', () => {
            post.style.backgroundColor = '#f9f9f9';
        });
        post.addEventListener('mouseout', () => {
            post.style.backgroundColor = '#fff';
        });
    });
});
