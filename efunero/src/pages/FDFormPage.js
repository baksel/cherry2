import { useEffect, useState } from "react";
import { auth} from "../config/firebase-config";
import FDForm from "../cmp/FDForm";


function FDFormPage( {stage, setStage} ) {

  //const [stage, setStage] = useState("loading");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  
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