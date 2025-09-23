import './FuneralItemAddInfo.css';
import AddInfoElement from './AddInfoElement'

function FuneralItemAddInfo(item) {
    const {address, Puhelinnumero, items} = item.item;
    

    return (
       <div className = "add-info"> 
        <h4 id="price-includes-h4"> Mitä hintaan sisältyy </h4>
        <div className="add-info-items-list"> 
            {/* square brackets convert item to an array (and makes map work) */}
            
            { (Object.entries(items)).map( (value, key) => { return (               
                    <AddInfoElement itemValue={value} itemKey={key} />
            )
            }) }

    
        </div>

        <div> <strong> Osoitetiedot:</strong> {address} </div>
        <div id="phone-number"> <strong> Puhelinnumero: </strong> <a href={`tel:${Puhelinnumero}`}> {Puhelinnumero} </a> </div>

       </div>
    );
}

export default FuneralItemAddInfo;