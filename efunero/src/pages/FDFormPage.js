import { useEffect, useState } from "react";
import { auth} from "../config/firebase-config";
import handleEmailSignin from "../hooks/handleEmailSignin"
import FDForm from "../cmp/FDForm";
import {onAuthStateChanged} from "firebase/auth";


function FDFormPage() {

  const [stage, setStage] = useState("loading");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  // Get email from URL
  useEffect(() => {

    const current_url = new URL( window.location.href);
    const emailFromUrl = current_url.searchParams.get("email") || "";
    setEmail(emailFromUrl);
    }, []);
  
  
  //console.log("stage is", stage);

  // Check if already logged in
  useEffect( () => {
      const unsub = onAuthStateChanged(auth, (user) => {
        if (user) {
            console.log("hababam", user);
            setStage("success");
            console.log("You've reached success stage but Stage is ", stage);
          } 
          
      });

      return () => unsub(); 
  }, []);
  // if hasn't logged in, run login procedure
  useEffect(() => {
    const _handleEmailSignIn = async () => {
      console.log("stage is: ", stage);


      if (stage === "success") {
        return


      }
      const { status, error } = await handleEmailSignin(auth, window.location.href, email);
      setStage(status);
      }
      _handleEmailSignIn();
  
  

  }, [email, stage]);

  console.log("stage is", stage);
  // ---------------- UI STATES ----------------

  if (stage === "loading") {
    return <p>Kirjaudutaan…</p>;
  }

  if (stage === "needEmail") {
    return (
      <div>
        <p>
          Syötä sähköpostiosoite uudelleen (jos avasit linkin eri laitteella):
        </p>
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
    );
  }

  if (stage === "unauthorized") {
    return (
      <div>
        <h3>Ei valtuutusta</h3>
        <p>
          Tätä sähköpostia ei ole valtuutettu käyttämään lomaketta.
        </p>
      </div>
    );
  }
    if (stage === "success") {
    return (
      <FDForm/>
    );
  }


  if (stage === "submitted") {
    return (
      <p> Moi </p>
    );
  }

  if (stage === "error") {
    return (
      <div>
        <h3>Virhe</h3>
        <p>{error || "Virheellinen tai vanhentunut linkki."}</p>
      </div>
    );
  }

  }


export default FDFormPage;