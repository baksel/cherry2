import './FuneralItems.css';
import FuneralItem from './FuneralItem';
import { useGetItems } from '../hooks/useGetItems';

function FuneralItems({searchAreaValue}) {
    const funeralData = useGetItems();
    console.log(funeralData)

// Make a call to Firebase to fetch funeral items and for each funeral item, pass it to FuneralItem component
// Question: How to send the data, which is parsed via Python, to Firebase? Also, how to fetch it?
// The "app" will have a backend, independent part that will handle the data fetching and sending to Firebase.
    return (
        <div className="FuneralItems">
            <h2>Funeral Items in {searchAreaValue} </h2>
            {funeralData.map( (item, idx) => { return (
              <FuneralItem item = {item} />
            )
            })}
            

        </div>
    );
}

export default FuneralItems;