import './App.css';
import Header from './cmp/Header';
import Footer from './cmp/Footer'; 
import {BrowserRouter as Router, Routes, Route} from  "react-router-dom"
import MainPage from "./pages/MainPage"
import FDLoginOrFormPage from './pages/FDLoginOrFormPage';
import FDFormPage from './pages/FDFormPage';

function App() {

  


  return (  
    <>
      <div className="App">
        <Router>
          <Header />
          <Routes>
            <Route path="/" element={<MainPage/>} />
            <Route path="/hautaustoimistoille" element={<FDLoginOrFormPage/>} />
            <Route path="/hautaustoimistoille/finish" element={<FDFormPage/>} />
            <Route path="*" element={<MainPage/>} />

          </Routes>
          
            <Footer /> 

      </Router>
      </div>
    </>
    
  );
}

export default App;
