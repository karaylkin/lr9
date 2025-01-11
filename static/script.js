const loginForm = document.getElementById('login-form');
 const loginButton = document.getElementById('login-button');
 const bonusInfo = document.getElementById('bonus-info');
 const errorMessage = document.getElementById('error-message');

 loginButton.addEventListener('click', async () => {
     const username = document.getElementById('username').value;
     const password = document.getElementById('password').value;

     const loginData = {
         username: username,
         password: password,
     };

     try {
         const response = await fetch('/login', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json',
             },
             body: JSON.stringify(loginData),
         });
         if (!response.ok) {
             const errorData = await response.json();
             errorMessage.textContent = `Error: ${errorData.message}`;
             errorMessage.style.display = 'block';
             return;
         }
         const data = await response.json();
         const token = data.token;
         localStorage.setItem('token', token);
         await getBonusInfo(token);
         loginForm.style.display = 'none';
         errorMessage.style.display = 'none';
     } catch (error) {
         errorMessage.textContent = `An error occurred: ${error}`;
         errorMessage.style.display = 'block';
     }
 });

 async function getBonusInfo(token) {
     try {
         const response = await fetch('/bonus', {
             method: 'GET',
             headers: {
                 'Authorization': `Bearer ${token}`,
                 'Content-Type': 'application/json'
             },
         });
         if (!response.ok) {
             const errorData = await response.json();
             errorMessage.textContent = `Error: ${errorData.message}`;
             errorMessage.style.display = 'block';
             return;
         }
         const data = await response.json();
         document.getElementById('username-display').textContent = data.username;
         document.getElementById('spending-display').textContent = data.current_spending;
         document.getElementById('level-display').textContent = data.cashback_level_name;
         document.getElementById('percent-display').textContent = data.cashback_percent;
         document.getElementById('next-level-name').textContent = data.next_level_name;
         document.getElementById('next-level-threshold').textContent = data.next_level_threshold === -1 ? "Max" : data.next_level_threshold;

         bonusInfo.style.display = 'block';
         errorMessage.style.display = 'none';
     } catch (error) {
         errorMessage.textContent = `An error occurred: ${error}`;
         errorMessage.style.display = 'block';
     }
 }

 window.addEventListener('load', async () => {
     const storedToken = localStorage.getItem('token');
     if (storedToken) {
         await getBonusInfo(storedToken);
         loginForm.style.display = 'none';
     }
 })
