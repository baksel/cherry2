import './App.css';
import Header from './cmp/Header';
//import SearchArea from './cmp/SearchArea';
import FuneralItems from './cmp/FuneralItems';
import Footer from './cmp/Footer'; 
import ThePitch from './cmp/ThePitch';
import { useState} from 'react';

function App() {

  // By default, the search area will have "Helsinki" as the value
  const [searchAreaValue, setSearchAreaValue] = useState("Helsinki");


  return (
    <>  
      <div className="App">
        <Header />
        <div className="App-body">
          <ThePitch  updateCurrentSearchValue = {setSearchAreaValue} />
          {/* <SearchArea updateCurrentSearchValue = {setSearchAreaValue}/> */}
          <FuneralItems searchAreaValue = {searchAreaValue}/>
        </div>
          <Footer /> 
      </div>
    </>
    
  );
}

export default App;
