import './ThePitch.css';


function ThePitch(updateCurrentSearchValue) {

    return (
        <div className="ThePitch">
             <h1> Valitse paikkakuntasi ja etsi edullisia hautaustoimisoja alueeltasi. <h2>Helppoa -- eikö? </h2> </h1>
            <p> Efunero on hautaustoimistojen vertailusivusto, joka auttaa sinua löytämään edullisimmat hautaustoimistot alueeltasi. </p>
             <input 
             className ="search-bar"
             type="text"
             placeholder="Search for items..."
             onKeyDown={(e) => {
                if (e.key === 'Enter') {
                    updateCurrentSearchValue(e.target.value);
                }
             }
            }
              />
        </div>
    );
}

export default ThePitch;