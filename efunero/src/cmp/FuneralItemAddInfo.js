import './FuneralItemAddInfo.css';

function FuneralItemAddInfo(item) {
    const {address, Puhelinnumero, items} = item.item;

    return (
       <ul className = "add-info"> 
        <li> Hintaan sisältyy: {items} </li>
        <li> Osoitetiedot: {address} </li>
        <li id="phone-number"> Puhelinnumero: <a href={`tel:${Puhelinnumero}`}> {Puhelinnumero} </a> </li>

       </ul>
    );
}

export default FuneralItemAddInfo;