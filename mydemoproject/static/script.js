document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.dataset.userId;
            fetch(`/delete_user/${userId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    document.getElementById(`user-${userId}`).remove();
                } else {
                    console.error('Failed to delete user.');
                }
            });
        });
    });

    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.dataset.userId;
            // Handle the edit functionality here (e.g., open a modal to edit the user)
        });
    });
});
