import { useEffect, useState } from "react";
import { auth, db } from "../config/firebase-config";
import handleEmailSignin from "../hooks/handleEmailSignin"

import {
  addDoc,
  collection,
  serverTimestamp,
} from "firebase/firestore";



function FDFormPage() {
    
    const [stage, setStage] = useState("loading");
    const [email, setEmail] = useState(
    window.localStorage.getItem("efunero_provider_email") || ""
    );
    const [error, setError] = useState("");
    
    
    useEffect(() => {
      const _handleEmailSignIn = async () => {
        const { status, error } = await handleEmailSignin(auth, window.location.href, email);
        setStage(status);
        console.log(status);
        console.log(error);
       }
       _handleEmailSignIn()
    
    

  }, [email]);

  const submit = async () => {
    setError("");
    try {
      await addDoc(collection(db, "providerSubmissions"), {
        submittedByEmail: auth.currentUser?.email || null,
        status: "pending",
        createdAt: serverTimestamp(),
      });

      setStage("submitted");
    } catch (e) {
      console.error(e);
      setError("Tietojen lähetys epäonnistui.");
    }
  };

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

  if (stage === "submitted") {
    return (
      <div>
        <h3>Kiitos!</h3>
        <p>
          Vastaanotimme tietonne. Saatte ilmoituksen, kun ne on tarkistettu ja
          hyväksytty.
        </p>
      </div>
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