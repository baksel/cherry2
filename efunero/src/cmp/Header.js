import logo from '../logo.svg';
import './Header.css';

function Header() {

    return (
        <header className="App-Header">
            <img src={logo} className="App-logo" alt="logo" />
            <h1>Welcome to Efunero</h1>
        </header>
    );
}

export default Header;