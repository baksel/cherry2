import ThePitch from "../cmp/ThePitch"
import FuneralItems from "../cmp/FuneralItems"
import {useState} from "react";

function MainPage() {

    const [searchAreaValue, setSearchAreaValue] = useState("Helsinki");
    return (
        <div className="App-body">            
                <ThePitch  updateCurrentSearchValue = {setSearchAreaValue} />
                <FuneralItems searchAreaValue = {searchAreaValue}/>
            
        </div>
    )


}


export default MainPage;