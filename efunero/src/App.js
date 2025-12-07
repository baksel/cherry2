import './App.css';
import Header from './cmp/Header';
//import SearchArea from './cmp/SearchArea';
import FuneralItems from './cmp/FuneralItems';
import Footer from './cmp/Footer'; 
import ThePitch from './cmp/ThePitch';
import { useState} from 'react';
import { useAuth } from './LoggedState';
import {BrowserRouter as Router, Routes, Route}from  "react-router-dom"


function App() {

  // By default, the search area will have "Helsinki" as the value
  const [searchAreaValue, setSearchAreaValue] = useState("Helsinki");
  const { isLoggedIn } = useAuth();


  return (  
    <>
      <div className="App">
        <Header />
        <div className="App-body">
          {isLoggedIn ? (
            <>
            <ThePitch  updateCurrentSearchValue = {setSearchAreaValue} />
            <FuneralItems searchAreaValue = {searchAreaValue}/>
            </>
          ) : (
      
            <h2> "Texting Context Sharing"</h2>
          )
        }
        </div>
          <Footer /> 
      </div>
    </>
    
  );
}

export default App;
