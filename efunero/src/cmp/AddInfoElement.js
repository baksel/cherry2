import './AddInfoElement.css';

var elementEmojiMap = {
    "Arkku"           : "⚰️",
    "Uurna"           : "⚱️",
    "Arkkulaite"      : "⚰️",
    "Arkkuunhuolto"   : "⚰️",
    "Järjestelykulut" : "🛠️",
    "Vaatteet"        : "👔"
};



function AddInfoElement( { itemKey, itemValue }) {
    const { isIncluded, additionalInfo } = itemValue[1];
    const serviceName = itemValue[0];

    return (
       <div className = "add-info-element"> 
       <div className="add-info-element-text"> {elementEmojiMap[serviceName]} {serviceName}  </div> 
       { isIncluded ? (
        
            <div className="add-info-element-check">  ✓  </div>  
       ) : (
            <div className="add-info-element-cross"> ✕ </div>  
       )}
        
    </div>
    );

        
        
}

export default AddInfoElement;