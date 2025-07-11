document.addEventListener('DOMContentLoaded', () => {
  document.body.addEventListener('click', async function (e) {
    if (e.target && e.target.id === 'logout-link') {
      e.preventDefault();
      alert("Logout clicked!");

      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const response = await fetch('/api/auth/logout/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken }),
            signal: AbortSignal.timeout(2000)
          });

          if (!response.ok) {
            console.warn('Logout API responded with status:', response.status);
          } else {
            console.log('Logout API success');
          }
        } catch (error) {
          console.warn('Logout API error:', error);
        }
      }

      // Always clear local storage and redirect
      localStorage.clear();
      window.location.href = '/';
    }
  });
});
