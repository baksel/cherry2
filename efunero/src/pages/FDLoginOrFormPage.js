import FDLoginPage from "./FDLoginPage";
import FDFormPage from "./FDFormPage";
import {useState, useEffect} from "react";
import {onAuthStateChanged} from "firebase/auth";
import {auth} from "../config/firebase-config"


function FDLoginOrFormPage() {
  const [stage, setStage] = useState("loading");
  const [isAuthRdy, setIsAuthRdy] = useState(false);

  useEffect( () => {

    const unsub = onAuthStateChanged(auth, (user) => {
      setIsAuthRdy(true);
      if (user) {
        setStage("success")
      }
    });

    return ( () => unsub() );



  }, []);

  if (!isAuthRdy) return ( <p> Loading... </p>);
  return (
    <>
      { stage !== "success"? <FDLoginPage /> : <FDFormPage/> }
    </>
  );
  
}


export default FDLoginOrFormPage;