'use strict';
//listen auth
auth.onAuthStateChanged(user => {
    console.log(user)
    if (user) {
        setUpNav(user);
    } else {
        setUpNav();
    }
})

//sign up
const signupForm = document.querySelector('#signup-form')
signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = signupForm['signup-email'].value;
    const password = signupForm['signup-password'].value;

    //sign up new user
    auth.createUserWithEmailAndPassword(email, password).then(cred => {
        $('#modal-signup').modal('hide')
        signupForm.reset()
    })
})

//logout
const logout = document.querySelector('#logout');
logout.addEventListener('click', (e) => {
    e.preventDefault();
    auth.signOut();
})

//login
const loginForm = document.querySelector('#login-form');
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = loginForm['login-email'].value;
    const password = loginForm['login-password'].value;

    auth.signInWithEmailAndPassword(email, password).then(cred => {
        $('#modal-login').modal('hide');
        loginForm.reset();
    })
})

function googleSignIn() {
    var base_provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithRedirect(base_provider);
}
