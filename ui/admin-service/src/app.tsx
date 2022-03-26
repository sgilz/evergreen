import Navbar from './components/navbar';
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'

export function App() {
  if (!localStorage.getItem('theme')) localStorage.setItem('theme', 'dark');

  return (
    <div className="relative flex flex-col w-full h-full">
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Home />}></Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}
