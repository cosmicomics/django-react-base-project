import { initializeApp } from "firebase/app";
import {
  getAuth,
  signInWithEmailAndPassword,
  onAuthStateChanged,
} from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDHaNKqO6hFcW0IG6fuuDj-gY7K66pc5H4",
  authDomain: "anti-fishing-extension.firebaseapp.com",
  projectId: "anti-fishing-extension",
  storageBucket: "anti-fishing-extension.appspot.com",
  messagingSenderId: "23108003724",
  appId: "1:23108003724:web:652bcb608661d1e60bd8a9",
  measurementId: "G-2MKXT4DS78",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Login with firebase
export const loginWithFirebase = async (email: string, password: string) => {
  const userCredential = await signInWithEmailAndPassword(
    auth,
    email,
    password
  );
  return userCredential.user.getIdToken(); // Récupérer le token Firebase
};
