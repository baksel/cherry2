import { useState, useContext } from 'react';
import './FPLoginButton.css';
import { useAuth} from "../LoggedState"

function FPLoginButton() {

    const { isLoggedIn, setIsLoggedIn }= useAuth();

    //const [isFPLoggedIn, setIsFPLoggedIn] = useState(false);

    return (
        <div className="fp-login-button-div"> 
            <button className = "fp-login-button" onClick = {() => setIsLoggedIn(!isLoggedIn) }> Hautaustoimistoille </button>
            <h1> { true ? "Hi" : "moi"}</h1>

        </div>
        
    );
}

export default FPLoginButton;