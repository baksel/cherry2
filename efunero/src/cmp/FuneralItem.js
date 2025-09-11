import './FuneralItem.css';

function FuneralItem(item) {
    const { funeral_provider, price, location, date, url } = item.item;
    return (
        <div className="FuneralItem"> 
            <div className="left-side">   
                <h2> {funeral_provider} </h2>
                <ul className="add-info">
                    <li> {location} </li>
                    <li> {date}     </li>
                    
                </ul>
                
            </div>
            <div className="right-side">
                <button className="price-button" onClick={() => window.open(url, "_blank")}> Hinnat alk. {price}€ </button>

            </div>
            
            
            
        </div>
    );
}

export default FuneralItem;