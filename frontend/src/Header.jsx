import './App.css'

function Header({date}) {
    return (
        <>
            <div className='header'>
                <h1 className='title'> LowStakes</h1>
                <div className='hotbar'>
                    <h3>{date}</h3>
                </div>
            </div>
        </>
    )
}

export default Header