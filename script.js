const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

signInButton.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});

const registerForm = document.getElementById('registerForm');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirmPassword');

registerForm.addEventListener('submit', (e) => {
    if (password.value !== confirmPassword.value) {
        e.preventDefault();
        alert(" Passwords do not match!");
    }
});
