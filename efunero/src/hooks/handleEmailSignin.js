import { isSignInWithEmailLink, signInWithEmailLink } from "firebase/auth";

async function handleEmailSignin(auth, href, email) {
  const ALLOWED_EMAILS = ["akselbektas@yahoo.co.uk", "jamesemmet@hotmail.com"];
  console.log(auth, href, email);
   try {
        if (!isSignInWithEmailLink(auth, href)) {
          
          return (
            {status: "Incorrect email"}
          )
        }

        // Happens if link is opened on another device
        if (!email) {
          console.log("Reached `opened another device'")
          
          return (  
            {status: "Openede another device"}
          )
        }

        const cleanEmail = email.trim().toLowerCase();

        const result = await signInWithEmailLink(
          auth,
          cleanEmail,
          href
        );

        window.localStorage.removeItem("efunero_provider_email");

        const signedInEmail = result.user?.email?.toLowerCase();

        if (!signedInEmail) {
            return (
              {status : "no_email_typed"}
          );
          
        }

        if (!ALLOWED_EMAILS.includes(signedInEmail)) {
          return (
            {status : "unauthorized"}
          );
          
        }
        
        return (
          {status: "success",
          email: signedInEmail}
        );

        
      } catch (e) {
        return (
          {status: "error",
            error : e.text
          }
        )
        
      }
    }
  export default handleEmailSignin;