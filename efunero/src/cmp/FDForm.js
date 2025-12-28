import {useState, useMemo} from "react"
import './FuneralItems.css';
import "./FDForm.css"


function FDForm() {
    const items = useMemo(() => [
            { key: "arkku", label: "Arkku" },
            { key: "uurna", label: "Uurna" },
            { key: "arkkukoriste", label: "Arkkukoriste" },
            { key: "kukat", label: "Kukat" },
            { key: "kuljetus", label: "Kuljetus" },
            { key: "toimistokulut", label: "Toimistokulut" },
            ],
            []
        );
        
    const [totalPrice, setTotalPrice] = useState("");
    const [contents, setContents] = useState(() =>
        Object.fromEntries(items.map((i) => [i.key, null]))
    );
    const [error, setError] = useState("");

    const setItemValue = (key, value) => {
        setContents((prev) => ({ ...prev, [key]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError("");

        const normalized = totalPrice.replace(",", ".").trim();
        const priceNumber = Number(normalized);

        if (!normalized || Number.isNaN(priceNumber) || priceNumber < 0) {
        setError("Syötä kelvollinen kokonaishinta.");
        return;
        }

        const unanswered = Object.values(contents).some((v) => v === null);
        if (unanswered) {
        setError("Valitse kyllä/ei jokaiselle riville.");
        return;
        }

        const payload = {
        totalPrice: priceNumber,
        itemsIncluded: contents,
        };

        if (typeof onSubmit === "function") {
        //onSubmit(payload);
        }
    };

    


    return (
        <div className="form-container">
            <div className="form-info">
            <h3> Ole hyvä ja täytä alla oleva lomake. </h3>
            <p className="form-info"> 
                 Tällä hetkellä keräämme hautauspaketin hintaa, 
                joka koostuu: 1) arkusta; 2) uurnasta; 3) arkkukoristeesta; 4) kukista (yksi kappale);
                5) yhdestä kuljetuksesta; ja 6) mahdollisista toimistokuluista. 

                Merkitsethän mikäli ilmoittamaasi hintaan ei sisälly kaikkia yllä mainittuja.
            </p>
            </div>

            

            <form className="fd-form" onSubmit={handleSubmit}>
                {/* PART 1 */}
                <div className="fd-form__section">
                    <label htmlFor="totalPrice">
                    Ilmoita kokonaishinta (€)
                    </label>
                    <input
                    id="totalPrice"
                    type="text"
                    inputMode="decimal"
                    value={totalPrice}
                    onChange={(e) => setTotalPrice(e.target.value)}
                    placeholder="Esim. 1990"
                    />
                </div>

                {/* PART 2 */}
                <div className="fd-form__radiobox">
                    <p>Mitkä osat sisältyvät pakettiin?</p>

                    <div className="fd-form__items">
                    {items.map((item) => (
                        <div key={item.key} className="fd-form__item-row">
                        <span className="fd-form__item-label">
                            {item.label}
                        </span>

                        <label>
                            <input
                            type="radio"
                            name={`included_${item.key}`}
                            checked={contents[item.key] === true}
                            onChange={() => setItemValue(item.key, true)}
                            />
                            Kyllä
                        </label>

                        <label>
                            <input
                            type="radio"
                            name={`included_${item.key}`}
                            checked={contents[item.key] === false}
                            onChange={() => setItemValue(item.key, false)}
                            />
                            Ei
                        </label>
                        </div>
                    ))}
                    </div>
                </div>

                {error && <p className="fd-form__error">{error}</p>}

                <button type="submit" className="fd-form__submit">
                    Lähetä
                </button>
            </form>
        </div>
    );

}

export default FDForm;