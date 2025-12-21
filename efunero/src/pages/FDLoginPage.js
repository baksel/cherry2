import { useState } from "react";
import { sendSignInLinkToEmail } from "firebase/auth";
import { auth } from "../config/firebase-config"

function FDLoginPage() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  const sendLink = async () => {
    setError("");
    const cleanEmail = email.trim().toLowerCase();
    if (!cleanEmail) {
      setError("Syötä sähköpostiosoite.");
      return;
    }

    try {
      const actionCodeSettings = {
        url: `${window.location.origin}/hautaustoimistoille/finish`,
        handleCodeInApp: true,
      };

      await sendSignInLinkToEmail(auth, cleanEmail, actionCodeSettings);
      window.localStorage.setItem("efunero_provider_email", cleanEmail);
      setSent(true);
    } catch (e) {
      console.error(e);
      setError("Linkin lähetys epäonnistui.");
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto" }}>
      <h2>Hautaustoimistoille</h2>

      {!sent ? (
        <>
          <p>Syötä sähköpostiosoitteesi. Lähetämme sinulle kirjautumislinkin.</p>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: "100%", padding: 10 }}
          />
          <button onClick={sendLink} style={{ marginTop: 12 }}>
            Lähetä kirjautumislinkki
          </button>
          {error && <p>{error}</p>}
        </>
      ) : (
        <p>Tarkista sähköposti ja klikkaa linkkiä.</p>
      )}
    </div>
  );
}


export default FDLoginPage;