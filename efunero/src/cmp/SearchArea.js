import './SearchArea.css';

function SearchArea({updateCurrentSearchValue}) {

    return (
        <div className="App-SearchArea">
            <h1>This is the TOWN <h2> "I am heading 2" </h2></h1>
            <input 
             type="text"
             placeholder="Search for items..."
             onKeyDown={(e) => {
                if (e.key === 'Enter') {
                    updateCurrentSearchValue(e.target.value);
                }
             }
            }
              />
            <small style={{color: '#666', marginTop: '1rem'}}>← SearchArea Component: Uses flex-direction: column</small>
        </div>
    );
}

export default SearchArea;