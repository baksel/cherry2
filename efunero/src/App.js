import './App.css';
import Header from './cmp/Header';
//import SearchArea from './cmp/SearchArea';
import Footer from './cmp/Footer'; 
//import { useState} from 'react';
//import { useAuth } from './LoggedState';
import {BrowserRouter as Router, Routes, Route} from  "react-router-dom"
import MainPage from "./pages/MainPage"
import FDFormPage from "./pages/FDFormPage"
import FDLoginPage from './pages/FDLoginPage';
import FDForm from './cmp/FDForm';

function App() {

  // By default, the search area will have "Helsinki" as the value
  
  //const { isLoggedIn } = useAuth();


  return (  
    <>
      <div className="App">
        <Router>
          <Header />
          <Routes>
            <Route path="/" element={<MainPage/>} />
            <Route path="/hautaustoimistoille" element={<FDLoginPage/>} />
            <Route path="/hautaustoimistoille/finish" element={<FDFormPage/>} />
            <Route path="/hautaustoimistoilleOLD" element={<FDForm/>} />
            <Route path="*" element={<MainPage/>} />

          </Routes>

          {/* <MainPage/> */}
            <Footer /> 

      </Router>
      </div>
    </>
    
  );
}

export default App;
