import logo from '../logo.svg';
import './Header.css';

function Header() {

    return (
        <header className="App-Header">
            <img src={logo} className="App-logo" alt="logo" />
            <h1>Welcome to Efunero</h1>
            <small style={{marginLeft: 'auto', color: '#666'}}>← Header Component: Uses flexbox with justify-content: flex-start</small>
        </header>
    );
}

export default Header;