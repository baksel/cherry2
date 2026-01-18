import { useEffect, useState } from "react";
import { auth} from "../config/firebase-config";
import handleEmailSignin from "../hooks/handleEmailSignin"
import FDForm from "../cmp/FDForm";


function FDFormPage( {stage, setStage} ) {

  //const [stage, setStage] = useState("loading");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  // Get email from URL
  useEffect(() => {

    const current_url = new URL( window.location.href);
    const emailFromUrl = current_url.searchParams.get("email") || "";
    setEmail(emailFromUrl);
    }, []);
  
  
  useEffect(() => {

    const _handleEmailSignIn = async () => {
      console.log("stage is: ", stage);

      // Run only the below if not success
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
 
    if (stage === "success") {
    return (
      <FDForm/>
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