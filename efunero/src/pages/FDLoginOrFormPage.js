import FDLoginPage from "./FDLoginPage";
import FDFormPage from "./FDFormPage";
import { useState, useEffect } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../config/firebase-config"
import handleEmailSignin from "../hooks/handleEmailSignin"

function FDLoginOrFormPage() {
  const [stage, setStage] = useState("loading");

  useEffect( () => {

    const unsub = onAuthStateChanged(auth, (user) => {
      if (user) {
        setStage("success")
      }
      else {
        setStage("not authenticated")
      }
      
    });
    console.log(stage);
    return ( () => unsub() );


  }, [stage]);

  
  useEffect(() => {

    const current_url = new URL( window.location.href);
    const emailFromUrl = current_url.searchParams.get("email") || "";


    const _handleEmailSignIn = async () => {
      console.log("stage is: ", stage);

      // Run only the below if not success
      if (stage === "success") {
        return
      }

      const { status, error } = await handleEmailSignin(auth, window.location.href, emailFromUrl);
      setStage(status);
    }

    _handleEmailSignIn();


  }, []);

  console.log("Status in FDLoginOrFormPage is: ", stage);

  if ( stage === "loading" ) return ( <p> Loading... </p>);
  return (
    <>
      { stage !== "success"? <FDLoginPage /> : <FDFormPage stage={stage} setStage={setStage}/> }
    </>
  );
  
}


export default FDLoginOrFormPage;