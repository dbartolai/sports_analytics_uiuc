import React, { useState, useEffect } from "react";
import './App.css'
import Header from './Header.jsx'
import Scoreboard  from "./Scoreboard.jsx";


function App() {

  const [date, setDate] = useState("")

  useEffect(()=>{
    fetch("http://127.0.0.1:5000/scoreboard").then((res) =>
        res.json().then((input) => {
        setDate(input['date'])
        })
    )
  }, [])
  
  return (
    <>
      <Header date = {date}/>
      <div className='app'>
        <Scoreboard/>
      </div>
    </>
  )
}

export default App
