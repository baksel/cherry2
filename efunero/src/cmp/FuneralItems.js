import './FuneralItems.css';
import FuneralItem from './FuneralItem';
import { useGetItems } from '../hooks/useGetItems';

function FuneralItems({searchAreaValue}) {
    const funeralData = useGetItems();
    console.log(funeralData)


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