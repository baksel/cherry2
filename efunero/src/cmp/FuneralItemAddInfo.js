import './FuneralItemAddInfo.css';
import AddInfoElement from './AddInfoElement'

function FuneralItemAddInfo(item) {
    const {address, Puhelinnumero, items} = item.item;
    

    return (
       <div className = "add-info"> 
        <h4> Mitä hintaan sisältyy </h4>
        <div className="add-info-items-list"> 
            {/* square brackets convert item to an array (and makes map work) */}
            
            { (Object.entries(items)).map( (value, key) => { return (               
                    <AddInfoElement itemValue={value} itemKey={key} />
            )
            }) }

    
        </div>

        <li> Osoitetiedot: {address} </li>
        <li id="phone-number"> Puhelinnumero: <a href={`tel:${Puhelinnumero}`}> {Puhelinnumero} </a> </li>

       </div>
    );
}

export default FuneralItemAddInfo;