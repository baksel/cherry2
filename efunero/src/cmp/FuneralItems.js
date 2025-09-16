import './FuneralItems.css';
import FuneralItem from './FuneralItem';
import { useGetItems } from '../hooks/useGetItems';

function FuneralItems({searchAreaValue}) {
    const funeralData = useGetItems();


    return (
        <div className="FuneralItems">
            <h2>Hautaustoimistot {searchAreaValue} </h2>
            {funeralData.map( (item, idx) => { return (
              <FuneralItem item = {item} />
            )
            })}
            

        </div>
    );
}

export default FuneralItems;