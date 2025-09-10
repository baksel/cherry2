import './FuneralItem.css';

function FuneralItem(textToDisplay) {

    return (
        <div className="FuneralItem" id = {textToDisplay.id}> 
            <h2>{textToDisplay.textToDisplay} </h2>
            <h2> If I get the theory right, this should appear on the side</h2>
            
        </div>
    );
}

export default FuneralItem;