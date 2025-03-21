import React, { useState, useEffect } from "react";
import './Game.css'
import Logos from "./Logos.jsx"


function Game({index}) {

    const [game, setGame] = useState({
        game_id: "",
        home: "",
        away: ""
    });

    useEffect(()=>{
        fetch("http://127.0.0.1:5000/scoreboard").then((res) =>
          res.json().then((input) => {
            const cur_game = input['games'][index]
            setGame({
              game_id: cur_game[0],
              home: cur_game[1],
              away: cur_game[2]
            })
          })
        )
    }, [])

    return(
        <>
        <div className = 'game'>
            <div className='teams'>
                <div className='logo-div'>
                    <img src={Logos[game.away]} className='logo'/>
                    <h4 className='symbol'>{game.away}</h4>
                </div>
                <div className='at-div'><h2 className='at'>@</h2></div>
                <div className='logo-div'>
                    <img src={Logos[game.home]} className='logo'/>
                    <h4 className='symbol'>{game.home}</h4>
                </div>
            </div>
            
        </div>
        </>
    )
}


function Scoreboard(){
    
    const [num, setNum] = useState(0);
    const [games, setGames] = useState([])


    useEffect(()=>{
        fetch("http://127.0.0.1:5000/scoreboard").then((res) =>
            res.json().then((input) => {
                console.log("Response: ")
                console.log(input['number'])
            const num = input['number']
            setNum(num)
            setGames(Array.from({ length: input['number'] }, (_, i) => 
                <Game index={i} key={`game_${i}`} />
            ));
            })
        )
    }, [])


    return (
        <>
        <div className='game-date'>
            <h2> Today's Games: </h2>
        </div>
        <div className='scoreboard'>
            {games}
        </div>
        </>
    )
}

export default Scoreboard