import './Header.css';
import FPLoginButton from './FPLoginButton.js';
import {Link} from  "react-router-dom"
function Header() {

    return (
        <header className="App-Header">
            <div>
                <Link to="/" className="links-main-page"> <h1 >Efunero</h1> </Link>
                <p>Efunero auttaa sinua löytämään edullisimmat hautaustoimistot alueellasi </p>
            </div>
            <Link to="/hautaustoimistoille" className="links" > <h1 id="hautaustoimistoille-id"> <FPLoginButton/> </h1> </Link>
        </header>
    );
}

export default Header;