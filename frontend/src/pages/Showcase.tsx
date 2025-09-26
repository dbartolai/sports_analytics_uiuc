import DrakeCard from "../components/DrakeCard"
import RyanCard from "../components/RyanCard"
import RoshanCard from "../components/RoshanCard"
import ShravanCard from "../components/ShravanCard"
import NewCard from "../components/NewCard"
import AaryanCard from "../components/AaryanCard"
import DevCard from "../components/DevCard"

function Showcase () {
    return (
        <div>
        <h1>Dev Showcase!</h1>
        
            <DrakeCard/>
            <RyanCard/>
            <RoshanCard/>
            <ShravanCard/>
            <AaryanCard />
            <DevCard />
            <NewCard />
            <p>Updates</p>
        </div>
    )
} 

export default Showcase