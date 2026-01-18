import FDLoginPage from "./FDLoginPage";
import FDFormPage from "./FDFormPage";
import {useState, useEffect} from "react";
import {onAuthStateChanged} from "firebase/auth";
import {auth} from "../config/firebase-config"


function FDLoginOrFormPage() {
  const [stage, setStage] = useState("loading");

  useEffect( () => {

    const unsub = onAuthStateChanged(auth, (user) => {
      if (user) {
        setStage("success")
      }
    });

    return ( () => unsub() );



  }, [stage]);
  console.log("Status in FDLoginOrFormPage is: ", stage);

  if ( stage === "loading" ) return ( <p> Loading... </p>);
  return (
    <>
      { stage !== "success"? <FDLoginPage /> : <FDFormPage stage={stage} setStage={setStage}/> }
    </>
  );
  
}


export default FDLoginOrFormPage;