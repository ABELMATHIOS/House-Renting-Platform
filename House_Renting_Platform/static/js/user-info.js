document.addEventListener('DOMContentLoaded', () => {
  const userName = localStorage.getItem('userName');
  const userEmail = localStorage.getItem('userEmail');

  if (userName) {
    const nameEl = document.getElementById('user-name');
    if (nameEl) nameEl.textContent = userName;
  }

  if (userEmail) {
    const emailEl = document.getElementById('user-email');
    if (emailEl) emailEl.textContent = userEmail;
  }
});
