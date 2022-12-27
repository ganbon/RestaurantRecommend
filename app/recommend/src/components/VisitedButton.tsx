import PopUp  from "./PopUp";
import React, { useState } from "react";



const VisitedButton = () => {
    const [showModal, setShowModal] = useState(false);
    const ShowModal = () => {
        setShowModal(true);
      };
    return (
        <>
        <button onClick={ShowModal}>ブックマーク</button>
        <PopUp showFlag={showModal} setShowModal={setShowModal} />
        </>
    ); 
};

export default VisitedButton;