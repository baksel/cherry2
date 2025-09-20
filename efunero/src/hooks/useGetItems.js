import {collection, getDocs } from 'firebase/firestore/lite';
import { db } from '../config/firebase-config';
import {useState, useEffect} from 'react';


export const useGetItems =  () => {
  
  const [firebaseData, setFireBaseData] = useState([]);
  

  async function testFirebase() {
    const testCollection = collection(db, 'funeral_providers_1');
    const dataSnapshot = await getDocs(testCollection);
    const dataList = dataSnapshot.docs.map(doc => doc.data());
    setFireBaseData(dataList);
  }

  
  useEffect( () => {
    testFirebase();

    
 
    
  }
    , []);

  return firebaseData;

  
};
  
