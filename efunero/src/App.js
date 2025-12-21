import './App.css';
import Header from './cmp/Header';
//import SearchArea from './cmp/SearchArea';
import Footer from './cmp/Footer'; 
//import { useState} from 'react';
import { useAuth } from './LoggedState';
import {BrowserRouter as Router, Routes, Route} from  "react-router-dom"
import MainPage from "./pages/MainPage"
import FDFormPage from "./pages/FDFormPage"

function App() {

  // By default, the search area will have "Helsinki" as the value
  
  const { isLoggedIn } = useAuth();


  return (  
    <>
      <div className="App">
        <Router>
          <Header />
          <Routes>
            <Route path="/" element={<MainPage/>} />
            <Route path="/hautaustoimistoille" element={<FDFormPage/>} />
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
