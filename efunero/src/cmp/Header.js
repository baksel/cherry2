import './Header.css';
import FPLoginButton from './FPLoginButton.js';
import {Link, NavLink} from  "react-router-dom"
function Header() {

    return (
        <header className="App-Header">
            <div>
                <h1>Efunero</h1>
                <p>Efunero auttaa sinua löytämään edullisimmat hautaustoimistot alueellasi </p>
            </div>
            <FPLoginButton />
        </header>
    );
}

export default Header;