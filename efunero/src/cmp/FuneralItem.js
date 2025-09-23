import './FuneralItem.css';
import FuneralItemAddInfo from './FuneralItemAddInfo.js';
import {useState} from 'react';
import { MdKeyboardArrowDown, MdKeyboardArrowUp } from 'react-icons/md';

function FuneralItem(item) {
    
    const { funeral_provider, price, url } = item.item;
    const [showMore, setShowMore] = useState(false);

    return (
        <div className="FuneralItem"> 

          <div className="basic-info">
              <div className="left-side">
                <div className="name-basic-container">
                      <h3> {funeral_provider} </h3>
                      <button
                        className="toggle-button"
                        onClick={() => setShowMore(!showMore)}
                        aria-label={showMore ? "Näytä vähemmän": "Näytä lisää"}
                      >
                        {showMore ? <MdKeyboardArrowUp /> : <MdKeyboardArrowDown />}

                      </button>
                </div>    
                    
                  
              </div>
              <div className="right-side">
                  <button className="price-button" onClick={() => window.open(url, "_blank")}> Hinnat alk. {price}€ </button>

              </div>
              
          </div>
          
          {showMore ? <FuneralItemAddInfo item={item.item}/> : null}
            
            
        </div>
    );
}

export default FuneralItem;