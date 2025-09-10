import './FuneralItems.css';
import FuneralItem from './FuneralItem';

function FuneralItems({searchAreaValue}) {
// Make a call to Firebase to fetch funeral items and for each funeral item, pass it to FuneralItem component
// Question: How to send the data, which is parsed via Python, to Firebase? Also, how to fetch it?
// The "app" will have a backend, independent part that will handle the data fetching and sending to Firebase.
    return (
        <div className="FuneralItems">
            <h2>Funeral Items in {searchAreaValue} </h2>
            <FuneralItem id = "aksel" textToDisplay = "Hello there, I see you're learning to fly"/>
            <FuneralItem textToDisplay = "Is it just me, or is the world of Box models fascinating?"/>
        </div>
    );
}

export default FuneralItems;