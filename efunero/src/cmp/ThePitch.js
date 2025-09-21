import './ThePitch.css';
import { useRef } from 'react';


function ThePitch({ updateCurrentSearchValue }) {
    let tempCityHolder = useRef("Helsinki");

    return (
        <div className="ThePitch">
            <i className="search-icon"> 🔍 </i>
             <h1 className="intro-text"> Löydä hautaustoimistot helposti alueellasi</h1>
             <div className="search-container">
                <select 
                    className="search-bar"
                    onChange={(e) => tempCityHolder.current = e.target.value}
                    defaultValue=""
                >
                    <option value="" disabled>Valitse paikkakunta...</option>
                    <option value="Helsinki">Helsinki</option>
                    <option value="Espoo">Espoo</option>
                </select>
                <button className="search-button"
                // Take the value from the select input and pass it to updateCurrentSearchValue
                    onClick={ () =>  updateCurrentSearchValue(tempCityHolder.current)}     
                    > 
                    Hae
                </button> 
            </div>



            </div>

        
    );
}

export default ThePitch;