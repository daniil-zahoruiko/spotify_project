import { useContext } from "react"
import {IoSettingsOutline} from "react-icons/io5"
import { SongsContext } from "../SongsData"
import "../styles/nav.css"

export const Nav = () =>{
    const {page:[,setCurrentPage]} = useContext(SongsContext)

    return(
        <nav className="desktop_nav">
            <ul>
                <li className="nav_outer nav_logo">
                    <div>
                        <p onClick={()=>setCurrentPage("home")}>HARMONIA</p>
                    </div>
                </li>
                <li className="nav_li nav_left">
                    <p onClick={()=>setCurrentPage("library")}>
                        Library
                    </p>
                </li>
                <li>
                    <svg onClick={()=>setCurrentPage("user_account")} className="user_logo" xmlns="http://www.w3.org/2000/svg" width="52" height="52" viewBox="0 0 52 52" fill="none">
                        <path d="M21 18V16C21 13.2386 23.2386 11 26 11V11C28.7614 11 31 13.2386 31 16V18" stroke="white" strokeWidth="2"/>
                        <path d="M14 37V32.5C14 26.1487 19.1487 21 25.5 21V21C31.8513 21 37 26.1487 37 32.5V37" stroke="white" strokeWidth="2"/>
                        <path d="M26 51C39.8071 51 51 39.8071 51 26C51 12.1929 39.8071 1 26 1C12.1929 1 1 12.1929 1 26C1 39.8071 12.1929 51 26 51Z" stroke="white" strokeWidth="2"/>
                    </svg>
                </li>
                <li className="nav_li nav_right">
                    <p onClick={()=>setCurrentPage("discover")}>
                        Discover
                    </p>
                </li>
                <li className="nav_outer nav_settings">
                    <div>
                        <IoSettingsOutline onClick={()=>setCurrentPage("settings")} className="settings_svg"/>
                    </div>
                </li>
            </ul>
        </nav>

    )
}