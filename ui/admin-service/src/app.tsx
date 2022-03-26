import Navbar from './components/Navbar';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import AssignRole from './pages/AssignRole';
import CreateRole from './pages/CreateRole';
import CreateUser from './pages/CreateUser';

export function App() {
  if (!localStorage.getItem('theme')) localStorage.setItem('theme', 'dark');

  return (
    <div className="relative flex flex-col w-full h-full">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/assign-role" element={<AssignRole />} />
          <Route path="/create-role" element={<CreateRole />} />
          <Route path="/create-user" element={<CreateUser />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
