// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBmDq5BAbGuS3Ae6uvzubDu0Z2dHzZj6Bk",
  authDomain: "squad-sixteen.firebaseapp.com",
  projectId: "squad-sixteen",
  storageBucket: "squad-sixteen.firebasestorage.app",
  messagingSenderId: "296189970655",
  appId: "1:296189970655:web:fb24fd1025703dbb5c816a",
  measurementId: "G-1C97LYBZ9S"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

let analytics = null;
if (typeof window !== "undefined") {
  // Verifica se estamos no lado do cliente
  analytics = getAnalytics(app);
}
const auth = getAuth(app);

export {app,auth };
